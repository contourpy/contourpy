#ifndef CONTOURPY_CONVERTER_H
#define CONTOURPY_CONVERTER_H

#include "common.h"

// Conversion of C++ object to return to python.
class Converter
{
public:
    static CodeArray convert_codes(
        unsigned long point_count, unsigned long cut_count,
        const unsigned long* cut_start, unsigned long subtract = 0);

    static CodeArray convert_codes_check_closed(
        unsigned long point_count, unsigned long cut_count,
        const unsigned long* cut_start, const double* points);

    static CodeArray convert_codes_check_closed_single(
        unsigned long point_count, const double* points);

    static OffsetArray convert_offsets(
        unsigned long offset_count, const unsigned long* start,
        unsigned long subtract = 0);

    static OffsetArray convert_offsets_nested(
        unsigned long offset_count, const unsigned long* start,
        const unsigned long* nested_start);

    static PointArray convert_points(
        unsigned long point_count, const double* start);
};

#endif // CONTOURPY_CONVERTER_H
