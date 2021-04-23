#ifndef CONTOURPY_INTERP_H
#define CONTOURPY_INTERP_H

#include <iosfwd>

// Enum for type of interpolation used to find intersection of contour lines
// with grid cell edges.

// C++11 scoped enum, must be fully qualified to use.
enum class Interp
{
    Linear = 1,
    Log = 2
};

std::ostream &operator<<(std::ostream &os, const Interp& interp);

#endif // CONTOURPY_INTERP_H
