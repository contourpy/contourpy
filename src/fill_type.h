#ifndef CONTOURPY_FILL_TYPE_H
#define CONTOURPY_FILL_TYPE_H

#include <iosfwd>

// C++11 scoped enum, must be fully qualified to use.
enum class FillType
{
    OuterCodes = 1,
    OuterOffsets = 2,
    CombinedCodes = 3,
    CombinedOffsets = 4,
    CombinedCodesOffsets = 5,
    CombinedOffsets2 = 6,
};

std::ostream &operator<<(std::ostream &os, const FillType& fill_type);

#endif // CONTOURPY_FILL_TYPE_H
