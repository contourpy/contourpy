#ifndef CONTOURPY_CONVERTER_H
#define CONTOURPY_CONVERTER_H

#include "common.h"

// Conversion of C++ object to return to python.
class Converter
{
public:
    static void convert_codes(
        unsigned long point_count, unsigned long cut_count,
        const unsigned long* cut_start, py::list& return_list,
        unsigned long subtract = 0);

    static void convert_codes_check_closed(
        unsigned long point_count, unsigned long cut_count,
        const unsigned long* cut_start, const double* points,
        py::list& return_list);

    static void convert_codes_check_closed_single(
        unsigned long point_count, const double* points, py::list& return_list);

    static void convert_offsets(
        unsigned long offset_count, const unsigned long* start,
        py::list& return_list, unsigned long subtract = 0);

    static void convert_offsets_nested(
        unsigned long offset_count, const unsigned long* start,
        const unsigned long* nested_start, py::list& return_list);

    static void convert_points(
        unsigned long point_count, const double* start, py::list& return_list);
};

#endif // CONTOURPY_CONVERTER_H
