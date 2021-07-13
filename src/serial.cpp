#include "base_impl.h"
#include "serial.h"

SerialContourGenerator::SerialContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
    const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type, Interp interp,
    index_t x_chunk_size, index_t y_chunk_size)
    : BaseContourGenerator(x, y, z, mask, corner_mask, line_type, fill_type, interp, x_chunk_size,
                           y_chunk_size)
{}

void SerialContourGenerator::march(std::vector<py::list>& return_lists)
{
    // Stage 1: Initialise cache z-levels and starting locations for whole domain.
    init_cache_levels_and_starts();

    // Stage 2: Trace contours.
    auto n_chunks = get_n_chunks();
    ChunkLocal local;
    for (index_t chunk = 0; chunk < n_chunks; ++chunk) {
        get_chunk_limits(chunk, local);
        if (is_filled())
            march_chunk_filled(local, return_lists);
        else
            march_chunk_lines(local, return_lists);
        local.clear();
    }
}
