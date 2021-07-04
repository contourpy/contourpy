#ifndef CONTOURPY_SERIAL_H
#define CONTOURPY_SERIAL_H

#include "base.h"

class SerialContourGenerator : public BaseContourGenerator<SerialContourGenerator>
{
public:
    SerialContourGenerator(
        const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
        const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type,
        Interp interp, index_t x_chunk_size, index_t y_chunk_size);

    friend class BaseContourGenerator;  ////////////// in public section or not?????? //////

private:
    // Write points and offsets/codes to output numpy arrays.
    void export_filled(
        ChunkLocal& local, const std::vector<double>& all_points,
        std::vector<py::list>& return_lists);

    void export_lines(
        ChunkLocal& local, const double* all_points_ptr, std::vector<py::list>& return_lists);

    void init_cache_levels_and_starts(const ChunkLocal& local);

    py::sequence march();

    void march_chunk_filled(ChunkLocal& local, std::vector<py::list>& return_lists);

    void march_chunk_lines(ChunkLocal& local, std::vector<py::list>& return_lists);
};

#endif // CONTOURPY_SERIAL_H
