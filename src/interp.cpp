#include "interp.h"
#include <iostream>

std::ostream &operator<<(std::ostream &os, const Interp& interp)
{
    switch (interp) {
        case Interp::Linear:
            os << "Linear";
            break;
        case Interp::Log:
            os << "Log";
            break;
    }
    return os;
}
