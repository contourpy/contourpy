#ifndef CONTOURPY_CONVERTER_H
#define CONTOURPY_CONVERTER_H

#include "common.h"

// Conversion of C++ object to return to python.
class Converter
{
public:
    static CodeArray convert_codes(
        count_t point_count, count_t cut_count, const offset_t* cut_start, offset_t subtract = 0);

    static CodeArray convert_codes_check_closed(
        count_t point_count, count_t cut_count, const offset_t* cut_start, const double* points);

    static CodeArray convert_codes_check_closed_single(count_t point_count, const double* points);

    static OffsetArray convert_offsets(
        count_t offset_count, const offset_t* start, offset_t subtract);

    static PointArray convert_points(count_t point_count, const double* start);

private:
    static void check_max_offset(count_t max_offset);
};

#endif // CONTOURPY_CONVERTER_H
