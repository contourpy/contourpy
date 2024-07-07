#include "util.h"
#include <cmath>
#include <thread>

namespace contourpy {

bool Util::_nan_loaded = false;

double Util::nan = 0.0;

void Util::ensure_nan_loaded()
{
    if (!_nan_loaded) {
        auto numpy = py::module_::import("numpy");
        nan = numpy.attr("nan").cast<double>();
        _nan_loaded = true;
    }
}

index_t Util::get_max_threads()
{
    return static_cast<index_t>(std::thread::hardware_concurrency());
}

bool Util::is_nan(double value)
{
    auto numpy = py::module_::import("numpy");
    auto isnan = numpy.attr("isnan");
    return isnan(value).cast<bool>();


    //return std::isnan(value);

}

} // namespace contourpy
