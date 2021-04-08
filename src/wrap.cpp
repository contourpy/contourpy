#include "common.h"
#include "mpl2014.h"
#include "serial.h"
#include "serial_corner.h"
#include "fill_type.h"

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
        .def("contour_lines", &mpl2014::Mpl2014ContourGenerator::contour_lines)
        .def_property_readonly_static(
            "fill_type",
            [](py::object /* self */) {return FillType::OuterCodes;})
        .def_property_readonly_static(
            "line_type",
            [](py::object /* self */) {return LineType::SeparateCodes;});

    py::class_<SerialContourGenerator>(m, "SerialContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      LineType,
                      FillType,
                      long,
                      long>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::arg("line_type"),
             py::arg("fill_type"),
             py::kw_only(),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0)
        .def("contour_filled", &SerialContourGenerator::contour_filled)
        .def("contour_lines", &SerialContourGenerator::contour_lines)
        .def("write_cache", &SerialContourGenerator::write_cache)
        .def_property_readonly(
            "chunk_count", &SerialContourGenerator::get_chunk_count)
        .def_property_readonly(
            "chunk_size", &SerialContourGenerator::get_chunk_size)
        .def_property_readonly(
            "fill_type", &SerialContourGenerator::get_fill_type)
        .def_property_readonly(
            "line_type", &SerialContourGenerator::get_line_type)
        .def_property_readonly_static(
            "default_fill_type",
            [](py::object /* self */) {
                return SerialContourGenerator::default_fill_type();
            })
        .def_property_readonly_static(
            "default_line_type",
            [](py::object /* self */) {
                return SerialContourGenerator::default_line_type();
            })
        .def_static(
            "supports_fill_type",
            &SerialContourGenerator::supports_fill_type)
        .def_static(
            "supports_line_type",
            &SerialContourGenerator::supports_line_type);

    py::class_<SerialCornerContourGenerator>(m, "SerialCornerContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      LineType,
                      FillType,
                      long,
                      long>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::arg("line_type"),
             py::arg("fill_type"),
             py::kw_only(),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0)
        .def("contour_filled", &SerialCornerContourGenerator::contour_filled)
        .def("contour_lines", &SerialCornerContourGenerator::contour_lines)
        .def("write_cache", &SerialCornerContourGenerator::write_cache)
        .def_property_readonly(
            "chunk_count", &SerialCornerContourGenerator::get_chunk_count)
        .def_property_readonly(
            "chunk_size", &SerialCornerContourGenerator::get_chunk_size)
        .def_property_readonly(
            "fill_type", &SerialCornerContourGenerator::get_fill_type)
        .def_property_readonly(
            "line_type", &SerialCornerContourGenerator::get_line_type)
        .def_property_readonly_static(
            "default_fill_type",
            [](py::object /* self */) {
                return SerialCornerContourGenerator::default_fill_type();
            })
        .def_property_readonly_static(
            "default_line_type",
            [](py::object /* self */) {
                return SerialCornerContourGenerator::default_line_type();
            })
        .def_static(
            "supports_fill_type",
            &SerialCornerContourGenerator::supports_fill_type)
        .def_static(
            "supports_line_type",
            &SerialCornerContourGenerator::supports_line_type);

    py::enum_<FillType>(m, "FillType")
        .value("OuterCodes", FillType::OuterCodes)
        .value("OuterOffsets", FillType::OuterOffsets)
        .value("ChunkCombinedCodes", FillType::ChunkCombinedCodes)
        .value("ChunkCombinedOffsets", FillType::ChunkCombinedOffsets)
        .value("ChunkCombinedCodesOffsets", FillType::ChunkCombinedCodesOffsets)
        .value("ChunkCombinedOffsets2", FillType::ChunkCombinedOffsets2)
        .export_values();

    py::enum_<LineType>(m, "LineType")
        .value("Separate", LineType::Separate)
        .value("SeparateCodes", LineType::SeparateCodes)
        .value("ChunkCombinedCodes", LineType::ChunkCombinedCodes)
        .value("ChunkCombinedOffsets", LineType::ChunkCombinedOffsets)
        .export_values();
}
