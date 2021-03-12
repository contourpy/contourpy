#include "fill_type.h"
#include <iostream>

std::ostream &operator<<(std::ostream &os, const FillType& fill_type)
{
    switch (fill_type) {
        case FillType::OuterCodes:
            os << "OuterCodes";
            break;
        case FillType::OuterOffsets:
            os << "OuterOffsets";
            break;
        case FillType::CombinedCodes:
            os << "CombinedCodes";
            break;
        case FillType::CombinedOffsets:
            os << "CombinedOffsets";
            break;
        case FillType::CombinedCodesOffsets:
            os << "CombinedCodesOffsets";
            break;
        case FillType::CombinedOffsets2:
            os << "CombinedOffsets2";
            break;
    }
    return os;
}
