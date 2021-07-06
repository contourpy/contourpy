#include "base_impl.h"
#include "threaded.h"
#include "util.h"
#include <thread>

ThreadedContourGenerator::ThreadedContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
    const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type, Interp interp,
    index_t x_chunk_size, index_t y_chunk_size, index_t n_threads)
    : BaseContourGenerator(x, y, z, mask, corner_mask, line_type, fill_type, interp, x_chunk_size,
                           y_chunk_size),
      _n_threads(limit_n_threads(n_threads, _n_chunks)),
      _next_chunk(0)
{}

index_t ThreadedContourGenerator::get_thread_count() const
{
    return _n_threads;
}

void ThreadedContourGenerator::init_cache_levels_and_starts(const ChunkLocal& local)
{
    CacheItem keep_mask =
        (_corner_mask ? MASK_EXISTS_ANY | MASK_BOUNDARY_N | MASK_BOUNDARY_E
                      : MASK_EXISTS_QUAD | MASK_BOUNDARY_N | MASK_BOUNDARY_E);

    index_t istart = local.istart > 1 ? local.istart : 0;
    index_t iend = local.iend;
    index_t jstart = local.jstart > 1 ? local.jstart : 0;
    index_t jend = local.jend;

    index_t j_final_start = jstart - 1;

    for (index_t j = jstart; j <= jend; ++j) {
        index_t quad = istart + j*_nx;
        const double* z_ptr = _z.data() + quad;
        bool start_in_row = false;

        // z-level of NW point not needed if in W-most column, otherwise read it
        // from cache as already calculated.  Do not read if from cache if it is
        // in another chunk, calculate it now instead.
        ZLevel z_nw = (istart == 0) ? 0 :
            (istart == local.istart && istart > 1 ? calc_z_level(*(z_ptr-1)) : Z_NW);

        // z-level of SW point not needed if in S-most row or W-most column,
        // otherwise read it from cache as already calculated.  Do not read if
        // from cache if it is in another chunk, calculate it now instead.
        ZLevel z_sw = (istart == 0 || j == 0) ? 0 :
            (j == jstart || (istart == local.istart && istart > 1) ?
                calc_z_level(*(z_ptr-_nx-1)) : Z_SW);

        for (index_t i = istart; i <= iend; ++i, ++quad, ++z_ptr) {
            _cache[quad] &= keep_mask;
            _cache[quad] |= MASK_SADDLE;

            // Cache z-level of NE point.
            ZLevel z_ne = 0;
            if (_filled && *z_ptr > _upper_level) {
                _cache[quad] |= MASK_Z_LEVEL_2;
                z_ne = 2;
            }
            else if (*z_ptr > _lower_level) {
                _cache[quad] |= MASK_Z_LEVEL_1;
                z_ne = 1;
            }

            // z-level of SE point not needed if in S-most row, otherwise read
            // it from cache as already calculated.  Do not read if from cache
            // if it is in another chunk, calculate it now instead.
            ZLevel z_se = (j == 0) ? 0 :
                (j == jstart ? calc_z_level(*(z_ptr-_nx)) : Z_SE);

            if (EXISTS_ANY(quad)) {
                if (_filled) {
                    if (EXISTS_N_AND_E_EDGES(quad)) {
                        if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw == 0 || SADDLE_Z_LEVEL(quad) == 0)) {
                            _cache[quad] |= MASK_START_N;  // N to E low.
                            start_in_row = true;
                        }
                        else if (z_nw == 2 && z_se == 2 && z_ne < 2 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw == 2 ||
                                  SADDLE_Z_LEVEL(quad) == 2)) {
                            _cache[quad] |= MASK_START_N;  // N to E high.
                            start_in_row = true;
                        }

                        if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                            _cache[quad] |= MASK_START_E;  // E to N low.
                            start_in_row = true;
                        }
                        else if (z_ne == 2 && z_nw < 2 && z_se < 2 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw < 2 || SADDLE_Z_LEVEL(quad) < 2)) {
                            _cache[quad] |= MASK_START_E;  // E to N high.
                            start_in_row = true;
                        }
                    }

                    if (BOUNDARY_S(quad) &&
                        ((z_sw == 2 && z_se < 2) || (z_sw == 0 && z_se > 0) || z_sw == 1)) {
                        _cache[quad] |= MASK_START_BOUNDARY_S;
                        start_in_row = true;
                    }

                    if (BOUNDARY_W(quad) &&
                        ((z_nw == 2 && z_sw < 2) || (z_nw == 0 && z_sw > 0) ||
                         (z_nw == 1 && (z_sw != 1 || EXISTS_NW_CORNER(quad))))) {
                        _cache[quad] |= MASK_START_BOUNDARY_W;
                        start_in_row = true;
                    }

                    if (EXISTS_ANY_CORNER(quad)) {
                        if (EXISTS_NE_CORNER(quad) &&
                            ((z_nw == 2 && z_se < 2) || (z_nw == 0 && z_se > 0) || z_nw == 1)) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                        else if (EXISTS_NW_CORNER(quad) &&
                                 ((z_sw == 2 && z_ne < 2) || (z_sw == 0 && z_ne > 0))) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                        else if (EXISTS_SE_CORNER(quad) && ((z_sw == 0 && z_se == 0 && z_ne > 0) ||
                                                            (z_sw == 2 && z_se == 2 && z_ne < 2))) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                        else if (EXISTS_SW_CORNER(quad) && z_nw == 1 && z_se == 1) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                    }

                    // Start following N boundary from E to W which is a hole.
                    // Required for an internal masked region which is a hole in
                    // a filled polygon.
                    if (BOUNDARY_N(quad) && EXISTS_N_EDGE(quad) && z_nw == 1 && z_ne == 1 &&
                        !START_HOLE_N(quad-1) && j % _y_chunk_size != 0 && j != _ny-1) {
                        _cache[quad] |= MASK_START_HOLE_N;
                        start_in_row = true;
                    }
                }
                else {  // !_filled
                    if (BOUNDARY_S(quad) && z_sw == 1 && z_se == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_S;
                        start_in_row = true;
                    }

                    if (BOUNDARY_W(quad) && z_nw == 1 && z_sw == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_W;
                        start_in_row = true;
                    }

                    if (BOUNDARY_E(quad) && z_se == 1 && z_ne == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_E;
                        start_in_row = true;
                    }

                    if (BOUNDARY_N(quad) && z_ne == 1 && z_nw == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_N;
                        start_in_row = true;
                    }

                    if (EXISTS_N_AND_E_EDGES(quad) && !BOUNDARY_N(quad) && !BOUNDARY_E(quad)) {
                        if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                            _cache[quad] |= MASK_START_E;  // E to N low.
                            start_in_row = true;
                        }
                        else if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw == 0 ||
                                  SADDLE_Z_LEVEL(quad) == 0)) {
                            _cache[quad] |= MASK_START_N;  // N to E low.
                            start_in_row = true;
                        }
                    }

                    if (EXISTS_ANY_CORNER(quad)) {
                        bool corner_start = false;
                        if (EXISTS_NW_CORNER(quad))
                            corner_start = (z_sw == 1 && z_ne == 0);
                        else if (EXISTS_NE_CORNER(quad))
                            corner_start = (z_nw == 1 && z_se == 0);
                        else if (EXISTS_SW_CORNER(quad))
                            corner_start = (z_se == 1 && z_nw == 0);
                        else  // EXISTS_SE_CORNER
                            corner_start = (z_ne == 1 && z_sw == 0);

                        if (corner_start) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                    }
                }
            }

            z_nw = z_ne;
            z_sw = z_se;
        } // i-loop.

        if (start_in_row)
            j_final_start = j;
        else if (j > 0)
            _cache[local.istart + j*_nx] |= MASK_NO_STARTS_IN_ROW;
    } // j-loop.

    if (j_final_start < local.jend) {
        //std::cout << "NO MORE STARTS j_final_start=" << j_final_start
          //  << " quad=" << local.istart + (j_final_start+1)*_nx << std::endl;
        _cache[local.istart + (j_final_start+1)*_nx] |= MASK_NO_MORE_STARTS;
    }
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
    // Each stage is performed on a chunk by chunk basis.  There is a barrier
    // between the two stages to synchronise the threads so that the cache setup
    // is complete before being used by the trace.
    _next_chunk = 0;      // Next available chunk index.
    _finished_count = 0;  // Count of threads that have finished the cache init.

    // Create (_n_threads-1) new worker threads.
    std::vector<std::thread> threads;
    threads.reserve(_n_threads);
    for (unsigned int i = 0; i < _n_threads-1; ++i)
        threads.emplace_back(
            &ThreadedContourGenerator::thread_function, this, std::ref(return_lists));

    thread_function(std::ref(return_lists));  // Main thread work.

    for (auto& thread : threads)
        thread.join();
    assert(_next_chunk == 2*_n_chunks);
    threads.clear();
}

void ThreadedContourGenerator::thread_function(std::vector<py::list>& return_lists)
{
    // Function that is executed by each of the threads.
    // _next_chunk starts at zero and increases up to 2*_n_chunks.  A thread in
    // need of work reads _next_chunk and incremements it, then processes that
    // chunk.  For _next_chunk < _n_chunks this is stage 1 (init cache levels
    // and starting locations) and for _next_chunk >= _n_chunks this is stage 2
    // (trace contours).  There is a synchronisation barrier between the two
    // stages so that the cache initialisation is complete before being used by
    // the contour trace.

    index_t chunk;
    ChunkLocal local;

    // Stage 1: Initialise cache z-levels and starting locations.
    while (true) {
        {
            std::lock_guard<std::mutex> guard(_chunk_mutex);
            if (_next_chunk < _n_chunks)
                chunk = _next_chunk++;
            else
                break;  // No more work to do.
        }

        get_chunk_limits(chunk, local);
        init_cache_levels_and_starts(local);
        local.clear();
    }

    {
        // Implementation of multithreaded barrier.  Each thread increments the
        // shared counter.  Last thread to finish notifies the other threads
        // that they can all continue.
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
            if (_next_chunk < 2*_n_chunks)
                chunk = _next_chunk++ - _n_chunks;
            else
                break;  // No more work to do.
        }

        get_chunk_limits(chunk, local);
        if (_filled)
            march_chunk_filled(local, return_lists);
        else
            march_chunk_lines(local, return_lists);
        local.clear();
    }
}
