#ifndef CONTOURPY_LINE_TYPE_H
#define CONTOURPY_LINE_TYPE_H

#include <iosfwd>

// C++11 scoped enum, must be fully qualified to use.
enum class LineType
{
    Separate = 0,
};

std::ostream &operator<<(std::ostream &os, const LineType& line_type);

#endif // CONTOURPY_LINE_TYPE_H
