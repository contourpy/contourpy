#include "common.h"
#include "mpl2014.h"

PYBIND11_MODULE(_contourpy, m) {
    m.doc() = "doc notes";

    py::class_<mpl2014::Mpl2014ContourGenerator>(m, "Mpl2014ContourGenerator")
        .def(py::init<const CoordinateArray&,
                      const CoordinateArray &,
                      const CoordinateArray&,
                      const MaskArray&,
                      bool,
                      long>())
        .def("create_contour",
             &mpl2014::Mpl2014ContourGenerator::create_contour)
        .def("create_filled_contour",
             &mpl2014::Mpl2014ContourGenerator::create_filled_contour);
}
