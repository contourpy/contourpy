#include "line_type.h"
#include <iostream>

LineType LineType_from_string(const std::string& string)
{
    if       (string == "Separate")
        return LineType::Separate;
    else if  (string == "SeparateCodes")
        return LineType::SeparateCodes;
    else if  (string == "ChunkCombinedCodes")
        return LineType::ChunkCombinedCodes;
    else if  (string == "ChunkCombinedOffsets")
        return LineType::ChunkCombinedOffsets;
    else
        throw std::invalid_argument("'" + string + "' is not a valid LineType");
}

std::ostream &operator<<(std::ostream &os, const LineType& line_type)
{
    switch (line_type) {
        case LineType::Separate:
            os << "Separate";
            break;
        case LineType::SeparateCodes:
            os << "SeparateCodes";
            break;
        case LineType::ChunkCombinedCodes:
            os << "ChunkCombinedCodes";
            break;
        case LineType::ChunkCombinedOffsets:
            os << "ChunkCombinedOffsets";
            break;
    }
    return os;
}
