#include "base_impl.h"
#include "threaded.h"
#include "util.h"
#include <thread>

ThreadedContourGenerator::ThreadedContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
    const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type,
    bool quad_as_tri, ZInterp z_interp, index_t x_chunk_size, index_t y_chunk_size,
    index_t n_threads)
    : BaseContourGenerator(x, y, z, mask, corner_mask, line_type, fill_type, quad_as_tri, z_interp,
                           x_chunk_size, y_chunk_size),
      _n_threads(limit_n_threads(n_threads, get_n_chunks())),
      _next_chunk(0)
{}

index_t ThreadedContourGenerator::get_thread_count() const
{
    return _n_threads;
}

index_t ThreadedContourGenerator::limit_n_threads(index_t n_threads, index_t n_chunks)
{
    index_t max_threads = std::max<index_t>(Util::get_max_threads(), 1);
    if (n_threads == 0)
        return std::min(max_threads, n_chunks);
    else
        return std::min({max_threads, n_chunks, n_threads});
}

void ThreadedContourGenerator::march(std::vector<py::list>& return_lists)
{
    // Each thread executes thread_function() which has two stages:
    //   1) Initialise cache z-levels and starting locations
    //   2) Trace contours
    // Each stage is performed on a chunk by chunk basis.  There is a barrier between the two stages
    // to synchronise the threads so the cache setup is complete before being used by the trace.
    _next_chunk = 0;      // Next available chunk index.
    _finished_count = 0;  // Count of threads that have finished the cache init.

    // Create (_n_threads-1) new worker threads.
    std::vector<std::thread> threads;
    threads.reserve(_n_threads);
    for (index_t i = 0; i < _n_threads-1; ++i)
        threads.emplace_back(
            &ThreadedContourGenerator::thread_function, this, std::ref(return_lists));

    thread_function(std::ref(return_lists));  // Main thread work.

    for (auto& thread : threads)
        thread.join();
    assert(_next_chunk == 2*get_n_chunks());
    threads.clear();
}

void ThreadedContourGenerator::thread_function(std::vector<py::list>& return_lists)
{
    // Function that is executed by each of the threads.
    // _next_chunk starts at zero and increases up to 2*_n_chunks.  A thread in need of work reads
    // _next_chunk and incremements it, then processes that chunk.  For _next_chunk < _n_chunks this
    // is stage 1 (init cache levels and starting locations) and for _next_chunk >= _n_chunks this
    // is stage 2 (trace contours).  There is a synchronisation barrier between the two stages so
    // that the cache initialisation is complete before being used by the contour trace.

    auto n_chunks = get_n_chunks();
    index_t chunk;
    ChunkLocal local;

    // Stage 1: Initialise cache z-levels and starting locations.
    while (true) {
        {
            std::lock_guard<std::mutex> guard(_chunk_mutex);
            if (_next_chunk < n_chunks)
                chunk = _next_chunk++;
            else
                break;  // No more work to do.
        }

        get_chunk_limits(chunk, local);
        init_cache_levels_and_starts(&local);
        local.clear();
    }

    {
        // Implementation of multithreaded barrier.  Each thread increments the shared counter.
        // Last thread to finish notifies the other threads that they can all continue.
        std::unique_lock<std::mutex> lock(_chunk_mutex);
        _finished_count++;
        if (_finished_count == _n_threads)
            _condition_variable.notify_all();
        else
            _condition_variable.wait(lock);
    }

    // Stage 2: Trace contours.
    while (true) {
        {
            std::lock_guard<std::mutex> guard(_chunk_mutex);
            if (_next_chunk < 2*n_chunks)
                chunk = _next_chunk++ - n_chunks;
            else
                break;  // No more work to do.
        }

        get_chunk_limits(chunk, local);
        march_chunk(local, return_lists);
        local.clear();
    }
}
