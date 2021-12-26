#ifndef CONTOURPY_FILL_TYPE_H
#define CONTOURPY_FILL_TYPE_H

#include <iosfwd>
#include <string>

// C++11 scoped enum, must be fully qualified to use.
enum class FillType
{
    OuterCodes = 201,
    OuterOffsets = 202,
    ChunkCombinedCodes = 203,
    ChunkCombinedOffsets = 204,
    ChunkCombinedCodesOffsets = 205,
    ChunkCombinedOffsets2 = 206,
};

FillType FillType_from_string(const std::string& string);

std::ostream &operator<<(std::ostream &os, const FillType& fill_type);

#endif // CONTOURPY_FILL_TYPE_H
