#include "converter.h"
#include "mpl_kind_code.h"

CodeArray Converter::convert_codes(
    unsigned long point_count, unsigned long cut_count,
    const unsigned long* cut_start, unsigned long subtract)
{
    py::size_t codes_shape[1] = {point_count};
    CodeArray py_codes(codes_shape);
    auto py_ptr = py_codes.mutable_data();

    std::fill(py_ptr + 1, py_ptr + point_count - 1, LINETO);
    for (unsigned long i = 0; i < cut_count-1; ++i) {
        py_ptr[*(cut_start + i) - subtract] = MOVETO;
        py_ptr[*(cut_start + i+1) - 1 - subtract] = CLOSEPOLY;
    }

    return py_codes;
}

CodeArray Converter::convert_codes_check_closed(
    unsigned long point_count, unsigned long cut_count,
    const unsigned long* cut_start, const double* check_closed)
{
    py::size_t codes_shape[1] = {point_count};
    CodeArray py_codes(codes_shape);
    auto py_ptr = py_codes.mutable_data();

    std::fill(py_ptr + 1, py_ptr + point_count, LINETO);
    for (unsigned long i = 0; i < cut_count-1; ++i) {
        auto start = *(cut_start + i);
        auto end = *(cut_start + i+1);
        py_ptr[start] = MOVETO;
        bool closed = check_closed[2*start] == check_closed[2*end-2] &&
                      check_closed[2*start+1] == check_closed[2*end-1];
        if (closed)
            py_ptr[end-1] = CLOSEPOLY;
    }

    return py_codes;
}

CodeArray Converter::convert_codes_check_closed_single(
    unsigned long point_count, const double* points)
{
    py::size_t codes_shape[1] = {point_count};
    CodeArray py_codes(codes_shape);
    auto py_ptr = py_codes.mutable_data();

    py_ptr[0] = MOVETO;
    auto start = points;
    auto end = points + 2*point_count;
    bool closed = *start == *(end-2) && *(start+1) == *(end-1);
    if (closed) {
        std::fill(py_ptr + 1, py_ptr + point_count - 1, LINETO);
        py_ptr[point_count-1] = CLOSEPOLY;
    }
    else
        std::fill(py_ptr + 1, py_ptr + point_count, LINETO);

    return py_codes;
}

OffsetArray Converter::convert_offsets(
    unsigned long offset_count, const unsigned long* start,
    unsigned long subtract)
{
    py::size_t offsets_shape[1] = {offset_count};
    OffsetArray py_offsets(offsets_shape);
    if (subtract == 0)
        std::copy(start, start + offset_count, py_offsets.mutable_data());
    else {
        auto py_ptr = py_offsets.mutable_data();
        for (unsigned long i = 0; i < offset_count; ++i)
            *py_ptr++ = *(start + i) - subtract;
    }

    return py_offsets;
}

OffsetArray Converter::convert_offsets_nested(
    unsigned long offset_count, const unsigned long* start,
    const unsigned long* nested_start)
{
    py::size_t offsets_shape[1] = {offset_count};
    OffsetArray py_offsets(offsets_shape);
    auto py_ptr = py_offsets.mutable_data();
    for (unsigned long i = 0; i < offset_count; ++i)
        *py_ptr++ = *(nested_start + *(start + i));

    return py_offsets;
}

PointArray Converter::convert_points(
    unsigned long point_count, const double* start)
{
    py::size_t points_shape[2] = {point_count, 2};
    PointArray py_points(points_shape);
    std::copy(start, start + 2*point_count, py_points.mutable_data());

    return py_points;
}
