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
        case FillType::ChunkCombinedCodes:
            os << "ChunkCombinedCodes";
            break;
        case FillType::ChunkCombinedOffsets:
            os << "ChunkCombinedOffsets";
            break;
        case FillType::ChunkCombinedCodesOffsets:
            os << "ChunkCombinedCodesOffsets";
            break;
        case FillType::ChunkCombinedOffsets2:
            os << "ChunkCombinedOffsets2";
            break;
    }
    return os;
}
