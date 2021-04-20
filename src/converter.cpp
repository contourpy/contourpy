#include "converter.h"
#include "mpl_kind_code.h"

CodeArray Converter::convert_codes(
    size_t point_count, size_t cut_count, const size_t* cut_start,
    size_t subtract)
{
    py::ssize_t codes_shape[1] = {static_cast<py::ssize_t>(point_count)};
    CodeArray py_codes(codes_shape);
    auto py_ptr = py_codes.mutable_data();

    std::fill(py_ptr + 1, py_ptr + point_count - 1, LINETO);
    for (decltype(cut_count) i = 0; i < cut_count-1; ++i) {
        py_ptr[*(cut_start + i) - subtract] = MOVETO;
        py_ptr[*(cut_start + i+1) - 1 - subtract] = CLOSEPOLY;
    }

    return py_codes;
}

CodeArray Converter::convert_codes_check_closed(
    size_t point_count, size_t cut_count, const size_t* cut_start,
    const double* check_closed)
{
    py::ssize_t codes_shape[1] = {static_cast<py::ssize_t>(point_count)};
    CodeArray py_codes(codes_shape);
    auto py_ptr = py_codes.mutable_data();

    std::fill(py_ptr + 1, py_ptr + point_count, LINETO);
    for (decltype(cut_count) i = 0; i < cut_count-1; ++i) {
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
    size_t point_count, const double* points)
{
    py::ssize_t codes_shape[1] = {static_cast<py::ssize_t>(point_count)};
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
    size_t offset_count, const size_t* start, size_t subtract)
{
    py::ssize_t offsets_shape[1] = {static_cast<py::ssize_t>(offset_count)};
    OffsetArray py_offsets(offsets_shape);
    if (subtract == 0)
        std::copy(start, start + offset_count, py_offsets.mutable_data());
    else {
        auto py_ptr = py_offsets.mutable_data();
        for (decltype(offset_count) i = 0; i < offset_count; ++i)
            *py_ptr++ = static_cast<OffsetArray::value_type>(*(start + i) - subtract);
    }

    return py_offsets;
}

OffsetArray Converter::convert_offsets_nested(
    size_t offset_count, const size_t* start, const size_t* nested_start)
{
    py::ssize_t offsets_shape[1] = {static_cast<py::ssize_t>(offset_count)};
    OffsetArray py_offsets(offsets_shape);
    auto py_ptr = py_offsets.mutable_data();
    for (decltype(offset_count) i = 0; i < offset_count; ++i)
        *py_ptr++ = static_cast<OffsetArray::value_type>(*(nested_start + *(start + i)));

    return py_offsets;
}

PointArray Converter::convert_points(size_t point_count, const double* start)
{
    py::ssize_t points_shape[2] = {static_cast<py::ssize_t>(point_count), 2};
    PointArray py_points(points_shape);
    std::copy(start, start + 2*point_count, py_points.mutable_data());

    return py_points;
}
