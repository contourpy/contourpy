#ifndef CONTOURPY_LINE_TYPE_H
#define CONTOURPY_LINE_TYPE_H

#include <iosfwd>
#include <string>

// C++11 scoped enum, must be fully qualified to use.
enum class LineType
{
    Separate = 101,
    SeparateCodes = 102,
    ChunkCombinedCodes = 103,
    ChunkCombinedOffsets = 104,
};

LineType LineType_from_string(const std::string& string);

std::ostream &operator<<(std::ostream &os, const LineType& line_type);

#endif // CONTOURPY_LINE_TYPE_H
