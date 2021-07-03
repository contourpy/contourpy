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
};

#endif // CONTOURPY_SERIAL_H
