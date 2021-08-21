#ifndef CONTOURPY_MPL_2005_H
#define CONTOURPY_MPL_2005_H

#include "common.h"
#include "mpl2005_original.h"

class Mpl2005ContourGenerator
{
public:
    Mpl2005ContourGenerator(
        const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
        const MaskArray& mask, index_t x_chunk_size, index_t y_chunk_size);

    // Non-copyable and non-moveable.
    Mpl2005ContourGenerator(const Mpl2005ContourGenerator& other) = delete;
    Mpl2005ContourGenerator(const Mpl2005ContourGenerator&& other) = delete;
    Mpl2005ContourGenerator& operator=(const Mpl2005ContourGenerator& other) = delete;
    Mpl2005ContourGenerator& operator=(const Mpl2005ContourGenerator&& other) = delete;

    ~Mpl2005ContourGenerator();

    py::tuple filled(const double& lower_level, const double& upper_level);

    py::tuple get_chunk_count() const;  // Return (y_chunk_count, x_chunk_count)
    py::tuple get_chunk_size() const;   // Return (y_chunk_size, x_chunk_size)

    py::tuple lines(const double& level);

private:
    CoordinateArray _x, _y, _z;
    MaskArray _mask;
    Csite *_site;
};

#endif // CONTOURPY_MPL_2005_H
