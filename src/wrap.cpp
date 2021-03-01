#include "common.h"
#include "mpl2014.h"
#include "serial.h"

PYBIND11_MODULE(_contourpy, m) {
    m.doc() = "doc notes";

    py::class_<mpl2014::Mpl2014ContourGenerator>(m, "Mpl2014ContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      bool,
                      long>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::kw_only(),
             py::arg("corner_mask") = true,
             py::arg("chunk_size") = 0)
        .def("contour_filled",
             &mpl2014::Mpl2014ContourGenerator::contour_filled)
        .def("contour_lines",
             &mpl2014::Mpl2014ContourGenerator::contour_lines);

    py::class_<SerialContourGenerator>(m, "SerialContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      long,
                      long>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::kw_only(),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0)
        .def("contour_filled", &SerialContourGenerator::contour_filled)
        .def("write_cache", &SerialContourGenerator::write_cache)
        .def_property_readonly("chunk_count",
                               &SerialContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size",
                               &SerialContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask",
                               &SerialContourGenerator::get_corner_mask);
}
