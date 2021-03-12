#ifndef CONTOURPY_COMMON_H
#define CONTOURPY_COMMON_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

// Input numpy array classes.
typedef py::array_t<double, py::array::c_style | py::array::forcecast> CoordinateArray;
typedef py::array_t<bool,   py::array::c_style | py::array::forcecast> MaskArray;

// Output numpy array classes.
typedef py::array_t<double>  PointArray;
typedef py::array_t<uint8_t> CodeArray;
typedef py::array_t<int32_t> OffsetArray;

#endif // CONTOURPY_COMMON_H
