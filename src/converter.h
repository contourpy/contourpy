#ifndef CONTOURPY_CONVERTER_H
#define CONTOURPY_CONVERTER_H

#include "common.h"

namespace contourpy {

// Conversion of C++ object to return to python.
class Converter
{
public:
    static CodeArray convert_codes(
        count_t point_count, count_t cut_count, const offset_t* cut_start, offset_t subtract = 0);

    // Create and populate codes array,
    static CodeArray convert_codes_check_closed(
        count_t point_count, count_t cut_count, const offset_t* cut_start, const double* points);

    // Populate codes array that has already been created.
    static void convert_codes_check_closed(
        count_t point_count, count_t cut_count, const offset_t* cut_start, const double* points,
        CodeArray::value_type* codes);

    // Create and populate codes array (single line loop/strip).
    static CodeArray convert_codes_check_closed_single(
        count_t point_count, const double* points);

    // Populate codes array that has already been created (single line loop/strip).
    static void convert_codes_check_closed_single(
        count_t point_count, const double* points, CodeArray::value_type* codes);

    static OffsetArray convert_offsets(
        count_t offset_count, const offset_t* start, offset_t subtract);

    // Create and populate points array,
    static PointArray convert_points(count_t point_count, const double* start);

    // Populate points array that has already been created.
    static void convert_points(count_t point_count, const double* start, double* points);

private:
    static void check_max_offset(count_t max_offset);
};

} // namespace contourpy

#endif // CONTOURPY_CONVERTER_H
