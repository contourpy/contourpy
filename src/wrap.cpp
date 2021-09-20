#include "base_impl.h"
#include "fill_type.h"
#include "line_type.h"
#include "mpl2005.h"
#include "mpl2014.h"
#include "serial.h"
#include "threaded.h"
#include "util.h"
#include "z_interp.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

static LineType mpl20xx_line_type = LineType::SeparateCodes;
static FillType mpl20xx_fill_type = FillType::OuterCodes;

PYBIND11_MODULE(_contourpy, m) {
    m.doc() = "doc notes";

    m.attr("CONTOURPY_DEBUG") = CONTOURPY_DEBUG;
    m.attr("CONTOURPY_CXX11") = CONTOURPY_CXX11;
    m.attr("__version__") = MACRO_STRINGIFY(CONTOURPY_VERSION);

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

    py::enum_<ZInterp>(m, "ZInterp")
        .value("Linear", ZInterp::Linear)
        .value("Log", ZInterp::Log)
        .export_values();

    m.def("max_threads", &Util::get_max_threads, "docs");

    py::class_<Mpl2005ContourGenerator>(m, "Mpl2005ContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      index_t,
                      index_t>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::kw_only(),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0)
        .def("filled", &Mpl2005ContourGenerator::filled)
        .def("lines", &Mpl2005ContourGenerator::lines)
        .def_property_readonly("chunk_count", &Mpl2005ContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size", &Mpl2005ContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask", []() {return false;})
        .def_property_readonly_static(
            "default_fill_type", [](py::object /* self */) {return mpl20xx_fill_type;})
        .def_property_readonly_static(
            "default_line_type", [](py::object /* self */) {return mpl20xx_line_type;})
        .def_property_readonly(
            "fill_type", [](py::object /* self */) {return mpl20xx_fill_type;})
        .def_property_readonly(
            "line_type", [](py::object /* self */) {return mpl20xx_line_type;})
        .def_property_readonly("quad_as_tri", []() {return false;})
        .def_static("supports_corner_mask", []() {return false;})
        .def_static(
            "supports_fill_type", [](FillType fill_type) {return fill_type == mpl20xx_fill_type;})
        .def_static(
            "supports_line_type", [](LineType line_type) {return line_type == mpl20xx_line_type;})
        .def_static("supports_quad_as_tri", []() {return false;})
        .def_static("supports_threads", []() {return false;})
        .def_static("supports_z_interp", []() {return false;});

    py::class_<mpl2014::Mpl2014ContourGenerator>(m, "Mpl2014ContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      bool,
                      index_t,
                      index_t>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::kw_only(),
             py::arg("corner_mask"),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0)
        .def("filled", &mpl2014::Mpl2014ContourGenerator::filled)
        .def("lines", &mpl2014::Mpl2014ContourGenerator::lines)
        .def_property_readonly("chunk_count", &mpl2014::Mpl2014ContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size", &mpl2014::Mpl2014ContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask", &mpl2014::Mpl2014ContourGenerator::get_corner_mask)
        .def_property_readonly_static(
            "default_fill_type", [](py::object /* self */) {return mpl20xx_fill_type;})
        .def_property_readonly_static(
            "default_line_type", [](py::object /* self */) {return mpl20xx_line_type;})
        .def_property_readonly(
            "fill_type", [](py::object /* self */) {return mpl20xx_fill_type;})
        .def_property_readonly(
            "line_type", [](py::object /* self */) {return mpl20xx_line_type;})
        .def_property_readonly("quad_as_tri", []() {return false;})
        .def_static("supports_corner_mask", []() {return true;})
        .def_static(
            "supports_fill_type", [](FillType fill_type) {return fill_type == mpl20xx_fill_type;})
        .def_static(
            "supports_line_type", [](LineType line_type) {return line_type == mpl20xx_line_type;})
        .def_static("supports_quad_as_tri", []() {return false;})
        .def_static("supports_threads", []() {return false;})
        .def_static("supports_z_interp", []() {return false;});

    py::class_<SerialContourGenerator>(m, "SerialContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      bool,
                      LineType,
                      FillType,
                      bool,
                      ZInterp,
                      index_t,
                      index_t>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::kw_only(),
             py::arg("corner_mask"),
             py::arg("line_type"),
             py::arg("fill_type"),
             py::arg("quad_as_tri"),
             py::arg("z_interp"),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0)
        .def("filled", &SerialContourGenerator::filled)
        .def("lines", &SerialContourGenerator::lines)
        .def("write_cache", &SerialContourGenerator::write_cache)
        .def_property_readonly("chunk_count", &SerialContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size", &SerialContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask", &SerialContourGenerator::get_corner_mask)
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
        .def_property_readonly("fill_type", &SerialContourGenerator::get_fill_type)
        .def_property_readonly("line_type", &SerialContourGenerator::get_line_type)
        .def_property_readonly("quad_as_tri", &SerialContourGenerator::get_quad_as_tri)
        .def_static("supports_corner_mask", []() {return true;})
        .def_static("supports_fill_type", &SerialContourGenerator::supports_fill_type)
        .def_static("supports_line_type", &SerialContourGenerator::supports_line_type)
        .def_static("supports_quad_as_tri", []() {return true;})
        .def_static("supports_threads", []() {return false;})
        .def_static("supports_z_interp", []() {return true;});

    py::class_<ThreadedContourGenerator>(m, "ThreadedContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray&,
                      const CoordinateArray&,
                      const MaskArray&,
                      bool,
                      LineType,
                      FillType,
                      bool,
                      ZInterp,
                      index_t,
                      index_t,
                      index_t>(),
             py::arg("x"),
             py::arg("y"),
             py::arg("z"),
             py::arg("mask"),
             py::kw_only(),
             py::arg("corner_mask"),
             py::arg("line_type"),
             py::arg("fill_type"),
             py::arg("quad_as_tri"),
             py::arg("z_interp"),
             py::arg("x_chunk_size") = 0,
             py::arg("y_chunk_size") = 0,
             py::arg("thread_count") = 0)
        .def("filled", &ThreadedContourGenerator::filled)
        .def("lines", &ThreadedContourGenerator::lines)
        .def("write_cache", &ThreadedContourGenerator::write_cache)
        .def_property_readonly("chunk_count", &ThreadedContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size", &ThreadedContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask", &ThreadedContourGenerator::get_corner_mask)
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
        .def_property_readonly("fill_type", &ThreadedContourGenerator::get_fill_type)
        .def_property_readonly("line_type", &ThreadedContourGenerator::get_line_type)
        .def_property_readonly("quad_as_tri", &ThreadedContourGenerator::get_quad_as_tri)
        .def_property_readonly("thread_count", &ThreadedContourGenerator::get_thread_count)
        .def_static("supports_corner_mask", []() {return true;})
        .def_static("supports_fill_type", &ThreadedContourGenerator::supports_fill_type)
        .def_static("supports_line_type", &ThreadedContourGenerator::supports_line_type)
        .def_static("supports_quad_as_tri", []() {return true;})
        .def_static("supports_threads", []() {return true;})
        .def_static("supports_z_interp", []() {return true;});
}
