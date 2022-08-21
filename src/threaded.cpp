#include "base_impl.h"
#include "converter.h"
#include "threaded.h"
#include "util.h"
#include <thread>

namespace contourpy {

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

void ThreadedContourGenerator::export_lines(ChunkLocal& local, std::vector<py::list>& return_lists)
{
    // Reimplementation of SerialContourGenerator::export_lines() to separate out the creation of
    // numpy arrays (which requires a thread lock) from the population of those arrays (which does
    // not). This minimises the time that the lock is used for.

    assert(local.total_point_count > 0);

    switch (get_line_type())
    {
        case LineType::Separate:
        case LineType::SeparateCode: {
            assert(!_direct_points && !_direct_line_offsets);

            bool separate_code = (get_line_type() == LineType::SeparateCode);
            std::vector<PointArray::value_type*> points_ptrs(local.line_count);
            std::vector<CodeArray::value_type*> codes_ptrs(separate_code ? local.line_count: 0);

            Lock lock(*this);
            for (decltype(local.line_count) i = 0; i < local.line_count; ++i) {
                auto point_start = local.line_offsets.start[i];
                auto point_end = local.line_offsets.start[i+1];
                auto point_count = point_end - point_start;
                assert(point_count > 1);

                index_t points_shape[2] = {static_cast<index_t>(point_count), 2};
                PointArray point_array(points_shape);
                return_lists[0].append(point_array);
                points_ptrs[i] = point_array.mutable_data();

                if (separate_code) {
                    index_t codes_shape = static_cast<index_t>(point_count);
                    CodeArray code_array(codes_shape);
                    return_lists[1].append(code_array);
                    codes_ptrs[i] = code_array.mutable_data();
                }
            }
            lock.unlock();

            for (decltype(local.line_count) i = 0; i < local.line_count; ++i) {
                auto point_start = local.line_offsets.start[i];
                auto point_end = local.line_offsets.start[i+1];
                auto point_count = point_end - point_start;
                assert(point_count > 1);

                Converter::convert_points(
                    point_count, local.points.start + 2*point_start, points_ptrs[i]);

                if (separate_code) {
                    Converter::convert_codes_check_closed_single(
                        point_count, local.points.start + 2*point_start, codes_ptrs[i]);
                }
            }
            break;
        }
        case LineType::ChunkCombinedCode: {
            assert(_direct_points && !_direct_line_offsets);
            // return_lists[0][local.chunk] already contains points.

            assert(local.total_point_count > 0);
            index_t codes_shape = static_cast<index_t>(local.total_point_count);

            Lock lock(*this);
            CodeArray code_array(codes_shape);
            lock.unlock();

            return_lists[1][local.chunk] = code_array;
            Converter::convert_codes_check_closed(
                local.total_point_count, local.line_count + 1, local.line_offsets.start,
                local.points.start, code_array.mutable_data());

            break;
        }
        case LineType::ChunkCombinedOffset:
            assert(_direct_points && _direct_line_offsets);
            // return_lists[0][local.chunk] already contains points.
            // return_lists[1][local.chunk] already contains line offsets.
            break;
    }
}

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

} // namespace contourpy
