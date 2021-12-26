#include "fill_type.h"
#include <iostream>

FillType FillType_from_string(const std::string& string)
{
    if       (string == "OuterCodes")
        return FillType::OuterCodes;
    else if  (string == "OuterOffsets")
        return FillType::OuterOffsets;
    else if  (string == "ChunkCombinedCodes")
        return FillType::ChunkCombinedCodes;
    else if  (string == "ChunkCombinedOffsets")
        return FillType::ChunkCombinedOffsets;
    else if  (string == "ChunkCombinedCodesOffsets")
        return FillType::ChunkCombinedCodesOffsets;
    else if  (string == "ChunkCombinedOffsets2")
        return FillType::ChunkCombinedOffsets2;
    else
        throw std::invalid_argument("'" + string + "' is not a valid FillType");
}

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
