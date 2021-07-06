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

private:
    friend class BaseContourGenerator;

    class Lock
    {
    public:
        explicit Lock(SerialContourGenerator& contour_generator)
        {}

        void unlock()
        {}
    };

    void init_cache_levels_and_starts(const ChunkLocal& local);

    void march(std::vector<py::list>& return_lists);
};

#endif // CONTOURPY_SERIAL_H
