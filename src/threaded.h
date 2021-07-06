#ifndef CONTOURPY_THREADED_H
#define CONTOURPY_THREADED_H

#include "base.h"
#include <condition_variable>
#include <mutex>

class ThreadedContourGenerator : public BaseContourGenerator<ThreadedContourGenerator>
{
public:
    ThreadedContourGenerator(
        const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
        const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type,
        Interp interp, index_t x_chunk_size, index_t y_chunk_size, index_t n_threads);

    index_t get_thread_count() const;

    friend class BaseContourGenerator;  ////////////// in public section or not?????? //////

private:
    class Lock : public std::unique_lock<std::mutex>
    {
    public:
        explicit Lock(ThreadedContourGenerator& contour_generator)
            : std::unique_lock<std::mutex>(contour_generator._python_mutex)
        {}
    };

    void init_cache_levels_and_starts(const ChunkLocal& local);

    static index_t limit_n_threads(index_t n_threads, index_t n_chunks);

    py::sequence march();

    void thread_function(std::vector<py::list>& return_lists);



    // Multithreading member variables.
    index_t _n_threads;        // Number of threads used.
    index_t _next_chunk;       // Next available chunk for thread to process.
    index_t _finished_count;   // Count of threads that have finished the cache init.
    std::mutex _chunk_mutex;   // Locks access to _next_chunk/_finished_count.
    std::mutex _python_mutex;  // Locks access to Python objects.
    std::condition_variable _condition_variable;
};

#endif // CONTOURPY_THREADED_H
