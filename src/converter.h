#ifndef CONTOURPY_CONVERTER_H
#define CONTOURPY_CONVERTER_H

#include "common.h"

// Conversion of C++ object to return to python.
class Converter
{
public:
    static CodeArray convert_codes(
        size_t point_count, size_t cut_count, const size_t* cut_start, size_t subtract = 0);

    static CodeArray convert_codes_check_closed(
        size_t point_count, size_t cut_count, const size_t* cut_start, const double* points);

    static CodeArray convert_codes_check_closed_single(size_t point_count, const double* points);

    static OffsetArray convert_offsets(
        size_t offset_count, const size_t* start, size_t subtract = 0);

    static OffsetArray convert_offsets_nested(
        size_t offset_count, const size_t* start, const size_t* nested_start);

    static PointArray convert_points(size_t point_count, const double* start);

private:
    static void check_max_offset(size_t max_offset);
};

#endif // CONTOURPY_CONVERTER_H
