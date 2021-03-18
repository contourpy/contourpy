#include "line_type.h"
#include <iostream>

std::ostream &operator<<(std::ostream &os, const LineType& line_type)
{
    switch (line_type) {
        case LineType::Separate:
            os << "Separate";
            break;
    }
    return os;
}
