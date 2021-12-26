#include "z_interp.h"
#include <iostream>

ZInterp ZInterp_from_string(const std::string& string)
{
    if      (string == "Linear")
        return ZInterp::Linear;
    else if (string == "Log")
        return ZInterp::Log;
    else
        throw std::invalid_argument("'" + string + "' is not a valid ZInterp");
}

std::ostream &operator<<(std::ostream &os, const ZInterp& z_interp)
{
    switch (z_interp) {
        case ZInterp::Linear:
            os << "Linear";
            break;
        case ZInterp::Log:
            os << "Log";
            break;
    }
    return os;
}
