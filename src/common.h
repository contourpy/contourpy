#ifndef CONTOURPY_COMMON_H
#define CONTOURPY_COMMON_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

typedef py::array_t<double, py::array::c_style | py::array::forcecast> CoordinateArray;
typedef py::array_t<bool,   py::array::c_style | py::array::forcecast> MaskArray;

#endif // CONTOURPY_COMMON_H
