#include "common.h"
#include "fill_type.h"
#include "interp.h"
#include "line_type.h"
#include "mpl2014.h"
#include "serial.h"
#include "threaded.h"

PYBIND11_MODULE(_contourpy, m) {
    m.doc() = "doc notes";

    py::class_<mpl2014::Mpl2014ContourGenerator>(m, "Mpl2014ContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      bool,
                      index_t>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::kw_only(),
             py::arg("corner_mask") = true,
             py::arg("chunk_size") = 0)
        .def("filled", &mpl2014::Mpl2014ContourGenerator::filled)
        .def("lines", &mpl2014::Mpl2014ContourGenerator::lines)
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
                      bool,
                      LineType,
                      FillType,
                      Interp,
                      index_t,
                      index_t>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::arg("corner_mask"),
             py::arg("line_type"),
             py::arg("fill_type"),
             py::arg("interp"),
             py::kw_only(),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0)
        .def("filled", &SerialContourGenerator::filled)
        .def("lines", &SerialContourGenerator::lines)
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

    py::class_<ThreadedContourGenerator>(m, "ThreadedContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      bool,
                      LineType,
                      FillType,
                      Interp,
                      index_t,
                      index_t,
                      index_t>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::arg("corner_mask"),
             py::arg("line_type"),
             py::arg("fill_type"),
             py::arg("interp"),
             py::kw_only(),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0,
             py::arg("thread_count") = 0)
        .def("filled", &ThreadedContourGenerator::filled)
        .def("lines", &ThreadedContourGenerator::lines)
        .def("write_cache", &ThreadedContourGenerator::write_cache)
        .def_property_readonly(
            "chunk_count", &ThreadedContourGenerator::get_chunk_count)
        .def_property_readonly(
            "chunk_size", &ThreadedContourGenerator::get_chunk_size)
        .def_property_readonly(
            "fill_type", &ThreadedContourGenerator::get_fill_type)
        .def_property_readonly(
            "line_type", &ThreadedContourGenerator::get_line_type)
        .def_property_readonly(
            "max_threads", &ThreadedContourGenerator::get_max_threads)
        .def_property_readonly(
            "thread_count", &ThreadedContourGenerator::get_thread_count)
        .def_property_readonly_static(
            "default_fill_type",
            [](py::object /* self */) {
                return ThreadedContourGenerator::default_fill_type();
            })
        .def_property_readonly_static(
            "default_line_type",
            [](py::object /* self */) {
                return ThreadedContourGenerator::default_line_type();
            })
        .def_static(
            "supports_fill_type",
            &ThreadedContourGenerator::supports_fill_type)
        .def_static(
            "supports_line_type",
            &ThreadedContourGenerator::supports_line_type);

    py::enum_<FillType>(m, "FillType")
        .value("OuterCodes", FillType::OuterCodes)
        .value("OuterOffsets", FillType::OuterOffsets)
        .value("ChunkCombinedCodes", FillType::ChunkCombinedCodes)
        .value("ChunkCombinedOffsets", FillType::ChunkCombinedOffsets)
        .value("ChunkCombinedCodesOffsets", FillType::ChunkCombinedCodesOffsets)
        .value("ChunkCombinedOffsets2", FillType::ChunkCombinedOffsets2)
        .export_values();

    py::enum_<Interp>(m, "Interp")
        .value("Linear", Interp::Linear)
        .value("Log", Interp::Log)
        .export_values();

    py::enum_<LineType>(m, "LineType")
        .value("Separate", LineType::Separate)
        .value("SeparateCodes", LineType::SeparateCodes)
        .value("ChunkCombinedCodes", LineType::ChunkCombinedCodes)
        .value("ChunkCombinedOffsets", LineType::ChunkCombinedOffsets)
        .export_values();
}
