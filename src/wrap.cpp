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

static LineType mpl20xx_line_type = LineType::SeparateCode;
static FillType mpl20xx_fill_type = FillType::OuterCode;

PYBIND11_MODULE(_contourpy, m) {
    m.doc() =
        "C++11 extension module wrapped using `pybind11`_.\n\n"
        ".. note::\n"
        "   It should not be necessary to access classes and functions in this extension module "
        "directly. Instead, :func:`contourpy.contour_generator` should be used to create "
        "ContourGenerator objects, and the enums (:class:`~contourpy.FillType`, "
        ":class:`~contourpy.LineType` and :class:`~contourpy.ZInterp`) and "
        ":func:`contourpy.max_threads` function are all available in the :mod:`contourpy` module.";

    m.attr("CONTOURPY_DEBUG") = CONTOURPY_DEBUG;
    m.attr("CONTOURPY_CXX11") = CONTOURPY_CXX11;
    m.attr("__version__") = MACRO_STRINGIFY(CONTOURPY_VERSION);

    py::enum_<FillType>(m, "FillType",
        "Enum used for ``fill_type`` keyword argument in :func:`~contourpy.contour_generator`.\n\n"
        "This controls the format of filled contour data returned from "
        ":meth:`~contourpy.SerialContourGenerator.filled`.")
        .value("OuterCode", FillType::OuterCode)
        .value("OuterOffset", FillType::OuterOffset)
        .value("ChunkCombinedCode", FillType::ChunkCombinedCode)
        .value("ChunkCombinedOffset", FillType::ChunkCombinedOffset)
        .value("ChunkCombinedCodeOffset", FillType::ChunkCombinedCodeOffset)
        .value("ChunkCombinedOffsetOffset", FillType::ChunkCombinedOffsetOffset)
        .export_values();

    py::enum_<LineType>(m, "LineType",
        "Enum used for ``line_type`` keyword argument in :func:`~contourpy.contour_generator`.\n\n"
        "This controls the format of contour line data returned from "
        ":meth:`~contourpy.SerialContourGenerator.lines`.")
        .value("Separate", LineType::Separate)
        .value("SeparateCode", LineType::SeparateCode)
        .value("ChunkCombinedCode", LineType::ChunkCombinedCode)
        .value("ChunkCombinedOffset", LineType::ChunkCombinedOffset)
        .export_values();

    py::enum_<ZInterp>(m, "ZInterp",
        "Enum used for ``z_interp`` keyword argument in :func:`~contourpy.contour_generator`\n\n"
        "This controls the interpolation used on ``z`` values to determine where contour lines "
        "intersect the edges of grid quads, and ``z`` values at quad centres.")
        .value("Linear", ZInterp::Linear)
        .value("Log", ZInterp::Log)
        .export_values();

    m.def("max_threads", &Util::get_max_threads,
        "Return the maximum number of threads, obtained from "
        "``std::thread::hardware_concurrency()``.\n\n"
        "This is the number of threads used by a multithreaded ContourGenerator if the kwarg "
        "``threads=0`` is passed to :func:`~contourpy.contour_generator`.");

    py::class_<Mpl2005ContourGenerator>(m, "Mpl2005ContourGenerator",
        "ContourGenerator corresponding to ``name=\"mpl2005\"``.\n\n"
        "This is the original 2005 Matplotlib algorithm. "
        "Does not support any of ``corner_mask``, ``quad_as_tri``, ``threads`` or ``z_interp``. "
        "Only supports ``line_type=LineType.SeparateCode`` and ``fill_type=FillType.OuterCode``. "
        "Only supports chunking for filled contours, not contour lines.\n\n"
        "This class implements the same interface as "
        ":class:`~contourpy._contourpy.SerialContourGenerator`.\n\n"
        ".. warning::\n"
        "   This algorithm is in ``contourpy`` for historic comparison. No new features or bug "
        "fixes will be added to it, except for security-related bug fixes.")
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
        .def("create_contour", &Mpl2005ContourGenerator::lines,
            "Synonym for :func:`~contourpy.Mpl2005ContourGenerator.lines` to provide backward "
            "compatibility with Matplotlib.")
        .def("create_filled_contour", &Mpl2005ContourGenerator::filled,
            "Synonym for :func:`~contourpy.Mpl2005ContourGenerator.filled` to provide backward "
            "compatibility with Matplotlib.")
        .def("filled", &Mpl2005ContourGenerator::filled)
        .def("lines", &Mpl2005ContourGenerator::lines)
        .def_property_readonly("chunk_count", &Mpl2005ContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size", &Mpl2005ContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask", [](py::object /* self */) {return false;})
        .def_property_readonly("fill_type", [](py::object /* self */) {return mpl20xx_fill_type;})
        .def_property_readonly("line_type", [](py::object /* self */) {return mpl20xx_line_type;})
        .def_property_readonly("quad_as_tri", [](py::object /* self */) {return false;})
        .def_property_readonly("thread_count", [](py::object /* self */) {return 1;})
        .def_property_readonly("z_interp", [](py::object /* self */) {return ZInterp::Linear;})
        .def_property_readonly_static("default_fill_type", [](py::object /* self */) {
            return mpl20xx_fill_type;})
        .def_property_readonly_static("default_line_type", [](py::object /* self */) {
            return mpl20xx_line_type;})
        .def_property_readonly("fill_type", [](py::object /* self */) {return mpl20xx_fill_type;})
        .def_property_readonly("line_type", [](py::object /* self */) {return mpl20xx_line_type;})
        .def_property_readonly("quad_as_tri", [](py::object /* self */) {return false;})
        .def_static("supports_corner_mask", []() {return false;})
        .def_static("supports_fill_type", [](FillType fill_type) {
            return fill_type == mpl20xx_fill_type;})
        .def_static("supports_line_type", [](LineType line_type) {
            return line_type == mpl20xx_line_type;})
        .def_static("supports_quad_as_tri", []() {return false;})
        .def_static("supports_threads", []() {return false;})
        .def_static("supports_z_interp", []() {return false;});

    py::class_<mpl2014::Mpl2014ContourGenerator>(m, "Mpl2014ContourGenerator",
        "ContourGenerator corresponding to ``name=\"mpl2014\"``.\n\n"
        "This is the 2014 Matplotlib algorithm, a replacement of the original 2005 algorithm that "
        "added ``corner_mask`` and made the code more maintainable. "
        "Only supports ``corner_mask``, does not support ``quad_as_tri``, ``threads`` or "
        "``z_interp``. \n"
        "Only supports ``line_type=LineType.SeparateCode`` and "
        "``fill_type=FillType.OuterCode``.\n\n"
        "This class implements the same interface as "
        ":class:`~contourpy._contourpy.SerialContourGenerator`.\n\n"
        ".. warning::\n"
        "   This algorithm is in ``contourpy`` for historic comparison. No new features or bug "
        "fixes will be added to it, except for security-related bug fixes.")
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
        .def("create_contour", &mpl2014::Mpl2014ContourGenerator::lines,
            "Synonym for :func:`~contourpy.Mpl2014ContourGenerator.lines` to provide backward "
            "compatibility with Matplotlib.")
        .def("create_filled_contour", &mpl2014::Mpl2014ContourGenerator::filled,
            "Synonym for :func:`~contourpy.Mpl2014ContourGenerator.filled` to provide backward "
            "compatibility with Matplotlib.")
        .def("filled", &mpl2014::Mpl2014ContourGenerator::filled)
        .def("lines", &mpl2014::Mpl2014ContourGenerator::lines)
        .def_property_readonly("chunk_count", &mpl2014::Mpl2014ContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size", &mpl2014::Mpl2014ContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask", &mpl2014::Mpl2014ContourGenerator::get_corner_mask)
        .def_property_readonly("fill_type", [](py::object /* self */) {return mpl20xx_fill_type;})
        .def_property_readonly("line_type", [](py::object /* self */) {return mpl20xx_line_type;})
        .def_property_readonly("quad_as_tri", [](py::object /* self */) {return false;})
        .def_property_readonly("thread_count", [](py::object /* self */) {return 1;})
        .def_property_readonly("z_interp", [](py::object /* self */) {return ZInterp::Linear;})
        .def_property_readonly_static("default_fill_type", [](py::object /* self */) {
            return mpl20xx_fill_type;})
        .def_property_readonly_static("default_line_type", [](py::object /* self */) {
            return mpl20xx_line_type;})
        .def_static("supports_corner_mask", []() {return true;})
        .def_static("supports_fill_type", [](FillType fill_type) {
            return fill_type == mpl20xx_fill_type;})
        .def_static("supports_line_type", [](LineType line_type) {
            return line_type == mpl20xx_line_type;})
        .def_static("supports_quad_as_tri", []() {return false;})
        .def_static("supports_threads", []() {return false;})
        .def_static("supports_z_interp", []() {return false;});

    py::class_<SerialContourGenerator>(m, "SerialContourGenerator",
        "ContourGenerator corresponding to ``name=\"serial\"``, the default algorithm for "
        "``contourpy``.\n\n"
        "Supports ``corner_mask``, ``quad_as_tri`` and ``z_interp`` but not ``threads``. "
        "Supports all options for ``line_type`` and ``fill_type``.")
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
        .def("_write_cache", &SerialContourGenerator::write_cache)
        .def("create_contour", &SerialContourGenerator::lines,
            "Synonym for :func:`~contourpy.SerialContourGenerator.lines` to provide backward "
            "compatibility with Matplotlib.")
        .def("create_filled_contour", &SerialContourGenerator::filled,
            "Synonym for :func:`~contourpy.SerialContourGenerator.filled` to provide backward "
            "compatibility with Matplotlib.")
        .def("filled", &SerialContourGenerator::filled,
            "Calculate and return filled contours between two levels.\n\n"
            "Args:\n"
            "    lower_level (float): Lower z-level of the filled contours.\n"
            "    upper_level (float): Upper z-level of the filled contours.\n"
            "Return:\n"
            "    Filled contour polygons as one or more sequences of numpy arrays. The exact "
            "format is determined by the ``fill_type`` used by the ``ContourGenerator``.")
        .def("lines", &SerialContourGenerator::lines,
            "Calculate and return contour lines at a particular level.\n\n"
            "Args:\n"
            "    level (float): z-level to calculate contours at.\n\n"
            "Return:\n"
            "    Contour lines (open line strips and closed line loops) as one or more sequences "
            "of numpy arrays. The exact format is determined by the ``line_type`` used by the "
            "``ContourGenerator``.")
        .def_property_readonly("chunk_count", &SerialContourGenerator::get_chunk_count,
            "Return tuple of (y, x) chunk counts.")
        .def_property_readonly("chunk_size", &SerialContourGenerator::get_chunk_size,
            "Return tuple of (y, x) chunk sizes.")
        .def_property_readonly("corner_mask", &SerialContourGenerator::get_corner_mask,
            "Return whether ``corner_mask`` is set or not.")
        .def_property_readonly("fill_type", &SerialContourGenerator::get_fill_type,
            "Return the ``FillType``.")
        .def_property_readonly("line_type", &SerialContourGenerator::get_line_type,
            "Return the ``LineType``.")
        .def_property_readonly("quad_as_tri", &SerialContourGenerator::get_quad_as_tri,
            "Return whether ``quad_as_tri`` is set or not.")
        .def_property_readonly("thread_count", [](py::object /* self */) {return 1;},
            "Return the number of threads used.")
        .def_property_readonly("z_interp", &SerialContourGenerator::get_z_interp,
            "Return the ``ZInterp``.")
        .def_property_readonly_static("default_fill_type", [](py::object /* self */) {
            return SerialContourGenerator::default_fill_type();},
            "Return the default ``FillType`` used by this algorithm.")
        .def_property_readonly_static("default_line_type", [](py::object /* self */) {
            return SerialContourGenerator::default_line_type();},
            "Return the default ``LineType`` used by this algorithm.")
        .def_static("supports_corner_mask", []() {return true;},
            "Return whether this algorithm supports ``corner_mask``.")
        .def_static("supports_fill_type", &SerialContourGenerator::supports_fill_type,
            "Return whether this algorithm supports a particular ``FillType``.")
        .def_static("supports_line_type", &SerialContourGenerator::supports_line_type,
            "Return whether this algorithm supports a particular ``LineType``.")
        .def_static("supports_quad_as_tri", []() {return true;},
            "Return whether this algorithm supports ``quad_as_tri``.")
        .def_static("supports_threads", []() {return false;},
            "Return whether this algorithm supports the use of threads.")
        .def_static("supports_z_interp", []() {return true;},
            "Return whether this algorithm supports ``z_interp`` values other than "
            "``ZInterp.Linear`` which all support.");

    py::class_<ThreadedContourGenerator>(m, "ThreadedContourGenerator",
        "ContourGenerator corresponding to ``name=\"threaded\"``, the multithreaded version of "
        ":class:`~contourpy._contourpy.SerialContourGenerator`.\n\n"
        "Supports ``corner_mask``, ``quad_as_tri`` and ``z_interp`` and ``threads``. "
        "Supports all options for ``line_type`` and ``fill_type``.\n\n"
        "This class implements the same interface as "
        ":class:`~contourpy._contourpy.SerialContourGenerator`.")
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
        .def("_write_cache", &ThreadedContourGenerator::write_cache)
        .def("create_contour", &ThreadedContourGenerator::lines,
            "Synonym for :func:`~contourpy.ThreadedContourGenerator.lines` to provide backward "
            "compatibility with Matplotlib.")
        .def("create_filled_contour", &ThreadedContourGenerator::filled,
            "Synonym for :func:`~contourpy.ThreadedContourGenerator.filled` to provide backward "
            "compatibility with Matplotlib.")
        .def("filled", &ThreadedContourGenerator::filled)
        .def("lines", &ThreadedContourGenerator::lines)
        .def_property_readonly("chunk_count", &ThreadedContourGenerator::get_chunk_count)
        .def_property_readonly("chunk_size", &ThreadedContourGenerator::get_chunk_size)
        .def_property_readonly("corner_mask", &ThreadedContourGenerator::get_corner_mask)
        .def_property_readonly("fill_type", &ThreadedContourGenerator::get_fill_type)
        .def_property_readonly("line_type", &ThreadedContourGenerator::get_line_type)
        .def_property_readonly("quad_as_tri", &ThreadedContourGenerator::get_quad_as_tri)
        .def_property_readonly("thread_count", &ThreadedContourGenerator::get_thread_count)
        .def_property_readonly("z_interp", &ThreadedContourGenerator::get_z_interp)
        .def_property_readonly_static("default_fill_type", [](py::object /* self */) {
            return ThreadedContourGenerator::default_fill_type();})
        .def_property_readonly_static("default_line_type", [](py::object /* self */) {
            return ThreadedContourGenerator::default_line_type();})
        .def_static("supports_corner_mask", []() {return true;})
        .def_static("supports_fill_type", &ThreadedContourGenerator::supports_fill_type)
        .def_static("supports_line_type", &ThreadedContourGenerator::supports_line_type)
        .def_static("supports_quad_as_tri", []() {return true;})
        .def_static("supports_threads", []() {return true;})
        .def_static("supports_z_interp", []() {return true;});
}
