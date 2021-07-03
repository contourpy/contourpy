#include "base_impl.h"
#include "serial.h"


SerialContourGenerator::SerialContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
    const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type, Interp interp,
    index_t x_chunk_size, index_t y_chunk_size)
    : BaseContourGenerator(x, y, z, mask, corner_mask, line_type, fill_type, interp, x_chunk_size,
                           y_chunk_size)
{}
