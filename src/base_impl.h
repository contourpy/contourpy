#ifndef CONTOURPY_BASE_IMPL_H
#define CONTOURPY_BASE_IMPL_H

#include "base.h"
#include "converter.h"
#include <iostream>


// Point indices from current quad index.
#define POINT_SW (quad-_nx-1)
#define POINT_SE (quad-_nx)
#define POINT_NW (quad-1)
#define POINT_NE (quad)


// CacheItem masks, only accessed directly to set.  To read, use accessors
// detailed below.  1 and 2 refer to level indices (lower and upper).
#define MASK_Z_LEVEL_1         (0x1 <<  0) // z > lower_level.
#define MASK_Z_LEVEL_2         (0x1 <<  1) // z > upper_level.
#define MASK_Z_LEVEL           (MASK_Z_LEVEL_1 | MASK_Z_LEVEL_2)
#define MASK_SADDLE_Z_LEVEL_1  (0x1 <<  2) // saddle z > lower_level
#define MASK_SADDLE_Z_LEVEL_2  (0x1 <<  3) // saddle z > upper_level
#define MASK_SADDLE            (MASK_SADDLE_Z_LEVEL_1 | MASK_SADDLE_Z_LEVEL_2)
#define MASK_BOUNDARY_N        (0x1 <<  4) // N edge of quad is a boundary.
#define MASK_BOUNDARY_E        (0x1 <<  5) // E edge of quad is a boundary.
// EXISTS_QUAD bit is always used, but the 4 EXISTS_CORNER are only used if
// _corner_mask is true.  Only one of EXISTS_QUAD or EXISTS_??_CORNER is ever
// set per quad.
#define MASK_EXISTS_QUAD       (0x1 <<  6) // All of quad exists (is not masked).
#define MASK_EXISTS_NE_CORNER  (0x1 <<  7) // NE corner exists, SW corner is masked.
#define MASK_EXISTS_NW_CORNER  (0x1 <<  8)
#define MASK_EXISTS_SE_CORNER  (0x1 <<  9)
#define MASK_EXISTS_SW_CORNER  (0x1 << 10)
#define MASK_EXISTS_ANY_CORNER (MASK_EXISTS_NW_CORNER | MASK_EXISTS_NE_CORNER | MASK_EXISTS_SW_CORNER | MASK_EXISTS_SE_CORNER)
#define MASK_EXISTS_ANY        (MASK_EXISTS_QUAD | MASK_EXISTS_ANY_CORNER)
#define MASK_START_N           (0x1 << 11) // N to E, filled and lines.
#define MASK_START_E           (0x1 << 12) // E to N, filled and lines.
#define MASK_START_BOUNDARY_N  (0x1 << 13) // Filled and lines.
#define MASK_START_BOUNDARY_E  (0x1 << 14) // Filled and lines.
#define MASK_START_BOUNDARY_S  (0x1 << 15) // Filled only.
#define MASK_START_BOUNDARY_W  (0x1 << 16) // Filled only.
#define MASK_START_HOLE_N      (0x1 << 17) // N boundary of EXISTS, E to W, filled only.
#define MASK_START_CORNER      (0x1 << 18) // Filled and lines.
#define MASK_ANY_START_FILLED  (MASK_START_N | MASK_START_E | MASK_START_BOUNDARY_W | MASK_START_BOUNDARY_S | MASK_START_HOLE_N | MASK_START_CORNER)
#define MASK_ANY_START_LINES   (MASK_START_N | MASK_START_E | MASK_START_BOUNDARY_N | MASK_START_BOUNDARY_E | MASK_START_BOUNDARY_S | MASK_START_BOUNDARY_W | MASK_START_CORNER)
#define MASK_LOOK_N            (0x1 << 19)
#define MASK_LOOK_S            (0x1 << 20)
#define MASK_NO_STARTS_IN_ROW  (0x1 << 21)
#define MASK_NO_MORE_STARTS    (0x1 << 22)

// Accessors for various CacheItem masks.
#define Z_LEVEL(quad)              (_cache[quad] & MASK_Z_LEVEL)
#define Z_NE                       Z_LEVEL(POINT_NE)
#define Z_NW                       Z_LEVEL(POINT_NW)
#define Z_SE                       Z_LEVEL(POINT_SE)
#define Z_SW                       Z_LEVEL(POINT_SW)
#define SADDLE_SET(quad)           ((_cache[quad] & MASK_SADDLE) != MASK_SADDLE)
#define SADDLE_Z_LEVEL(quad)       (SADDLE_SET(quad) ? ((_cache[quad] & MASK_SADDLE) >> 2) : calc_z_level_mid(quad))
#define BOUNDARY_N(quad)           (_cache[quad] & MASK_BOUNDARY_N)
#define BOUNDARY_E(quad)           (_cache[quad] & MASK_BOUNDARY_E)
#define BOUNDARY_S(quad)           (_cache[quad-_nx] & MASK_BOUNDARY_N)
#define BOUNDARY_W(quad)           (_cache[quad-1] & MASK_BOUNDARY_E)
#define EXISTS_QUAD(quad)          (_cache[quad] & MASK_EXISTS_QUAD)
#define EXISTS_NE_CORNER(quad)     (_cache[quad] & MASK_EXISTS_NE_CORNER)
#define EXISTS_NW_CORNER(quad)     (_cache[quad] & MASK_EXISTS_NW_CORNER)
#define EXISTS_SE_CORNER(quad)     (_cache[quad] & MASK_EXISTS_SE_CORNER)
#define EXISTS_SW_CORNER(quad)     (_cache[quad] & MASK_EXISTS_SW_CORNER)
#define EXISTS_ANY(quad)           (_cache[quad] & MASK_EXISTS_ANY)
#define EXISTS_NONE(quad)          (EXISTS_ANY(quad) == 0)
#define EXISTS_ANY_CORNER(quad)    (_cache[quad] & MASK_EXISTS_ANY_CORNER)
#define EXISTS_N_EDGE(quad)        (_cache[quad] & (MASK_EXISTS_QUAD | MASK_EXISTS_NW_CORNER | MASK_EXISTS_NE_CORNER))
#define EXISTS_E_EDGE(quad)        (_cache[quad] & (MASK_EXISTS_QUAD | MASK_EXISTS_NE_CORNER | MASK_EXISTS_SE_CORNER))
#define EXISTS_S_EDGE(quad)        (_cache[quad] & (MASK_EXISTS_QUAD | MASK_EXISTS_SW_CORNER | MASK_EXISTS_SE_CORNER))
#define EXISTS_W_EDGE(quad)        (_cache[quad] & (MASK_EXISTS_QUAD | MASK_EXISTS_NW_CORNER | MASK_EXISTS_SW_CORNER))
#define EXISTS_N_AND_E_EDGES(quad) (_cache[quad] & (MASK_EXISTS_QUAD | MASK_EXISTS_NE_CORNER))
// Note that EXISTS_NE_CORNER(quad) is equivalent to BOUNDARY_SW(quad), etc.
#define START_N(quad)              (_cache[quad] & MASK_START_N)
#define START_E(quad)              (_cache[quad] & MASK_START_E)
#define START_BOUNDARY_N(quad)     (_cache[quad] & MASK_START_BOUNDARY_N)
#define START_BOUNDARY_E(quad)     (_cache[quad] & MASK_START_BOUNDARY_E)
#define START_BOUNDARY_S(quad)     (_cache[quad] & MASK_START_BOUNDARY_S)
#define START_BOUNDARY_W(quad)     (_cache[quad] & MASK_START_BOUNDARY_W)
#define START_HOLE_N(quad)         (_cache[quad] & MASK_START_HOLE_N)
#define START_CORNER(quad)         (_cache[quad] & MASK_START_CORNER)
#define ANY_START_FILLED(quad)     (_cache[quad] & MASK_ANY_START_FILLED)
#define ANY_START_LINES(quad)      (_cache[quad] & MASK_ANY_START_LINES)
#define LOOK_N(quad)               (_cache[quad] & MASK_LOOK_N)
#define LOOK_S(quad)               (_cache[quad] & MASK_LOOK_S)
#define NO_STARTS_IN_ROW(quad)     (_cache[quad] & MASK_NO_STARTS_IN_ROW)
#define NO_MORE_STARTS(quad)       (_cache[quad] & MASK_NO_MORE_STARTS)


template <typename Derived>
BaseContourGenerator<Derived>::BaseContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
    const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type, Interp interp,
    index_t x_chunk_size, index_t y_chunk_size)
    : _x(x),
      _y(y),
      _z(z),
      _nx(_z.ndim() > 1 ? _z.shape(1) : 0),
      _ny(_z.ndim() > 0 ? _z.shape(0) : 0),
      _n(_nx*_ny),
      _x_chunk_size(x_chunk_size > 0 ? std::min(x_chunk_size, _nx-1) : _nx-1),
      _y_chunk_size(y_chunk_size > 0 ? std::min(y_chunk_size, _ny-1) : _ny-1),
      _nx_chunks(static_cast<index_t>(std::ceil((_nx-1.0) / _x_chunk_size))),
      _ny_chunks(static_cast<index_t>(std::ceil((_ny-1.0) / _y_chunk_size))),
      _n_chunks(_nx_chunks*_ny_chunks),
      _corner_mask(corner_mask),
      _line_type(line_type),
      _fill_type(fill_type),
      _interp(interp),
      _cache(new CacheItem[_n]),
      _filled(false),
      _lower_level(0.0),
      _upper_level(0.0),
      _identify_holes(false),
      _return_list_count(0)
{
    if (_x.ndim() != 2 || _y.ndim() != 2 || _z.ndim() != 2)
        throw std::invalid_argument("x, y and z must all be 2D arrays");

    if (_x.shape(1) != _nx || _x.shape(0) != _ny ||
        _y.shape(1) != _nx || _y.shape(0) != _ny)
        throw std::invalid_argument("x, y and z arrays must have the same shape");

    if (_nx < 2 || _ny < 2)
        throw std::invalid_argument("x, y and z must all be at least 2x2 arrays");

    if (mask.ndim() != 0) {  // ndim == 0 if mask is not set, which is valid.
        if (mask.ndim() != 2)
            throw std::invalid_argument("mask array must be a 2D array");

        if (mask.shape(1) != _nx || mask.shape(0) != _ny)
            throw std::invalid_argument(
                "If mask is set it must be a 2D array with the same shape as z");
    }

    if (!supports_line_type(line_type))
        throw std::invalid_argument("Unsupported LineType");

    if (!supports_fill_type(fill_type))
        throw std::invalid_argument("Unsupported FillType");

    if (x_chunk_size < 0 || y_chunk_size < 0)  // Check inputs, not calculated.
        throw std::invalid_argument("chunk_sizes cannot be negative");

    init_cache_grid(mask);
}

template <typename Derived>
BaseContourGenerator<Derived>::~BaseContourGenerator()
{
    delete [] _cache;
}

template <typename Derived>
typename BaseContourGenerator<Derived>::ZLevel BaseContourGenerator<Derived>::calc_z_level_mid(
    index_t quad)
{
    assert(quad >= 0 && quad < _n);

    double zmid = 0.25*(get_point_z(quad-_nx-1) + get_point_z(quad-_nx) +
                        get_point_z(quad-1) + get_point_z(quad));

    _cache[quad] &= ~MASK_SADDLE;  // Clear saddle bits.

    ZLevel ret = 0;
    if (_filled && zmid > _upper_level) {
        _cache[quad] |= MASK_SADDLE_Z_LEVEL_2;
        ret = 2;
    }
    else if (zmid > _lower_level) {
        _cache[quad] |= MASK_SADDLE_Z_LEVEL_1;
        ret = 1;
    }

    return ret;
}

template <typename Derived>
void BaseContourGenerator<Derived>::closed_line(
    const Location& start_location, OuterOrHole outer_or_hole, ChunkLocal& local)
{
    assert(is_quad_in_chunk(start_location.quad, local));

    Location location = start_location;
    bool finished = false;
    size_t point_count = 0;

    if (outer_or_hole == Hole && local.pass == 0 && _identify_holes)
        set_look_flags(start_location.quad);

    while (!finished) {
        if (location.on_boundary)
            finished = follow_boundary(location, start_location, local, point_count);
        else
            finished = follow_interior(location, start_location, local, point_count);
        location.on_boundary = !location.on_boundary;
    }

    if (local.pass > 0) {
        local.line_offsets[local.line_count] = local.total_point_count;
        if (outer_or_hole == Outer && _identify_holes) {
            size_t outer_count = local.line_count - local.hole_count;
            local.outer_offsets[outer_count] = local.line_count;
        }
    }

    local.total_point_count += point_count;
    local.line_count++;
    if (outer_or_hole == Hole)
        local.hole_count++;
}

template <typename Derived>
void BaseContourGenerator<Derived>::closed_line_wrapper(
    const Location& start_location, OuterOrHole outer_or_hole, ChunkLocal& local)
{
    assert(is_quad_in_chunk(start_location.quad, local));

    if (local.pass == 0 || !_identify_holes) {
        closed_line(start_location, outer_or_hole, local);
    }
    else {
        assert(outer_or_hole == Outer);
        local.look_up_quads.clear();

        closed_line(start_location, outer_or_hole, local);

        for (size_t i = 0; i < local.look_up_quads.size(); ++i) {
            // Note that the collection can increase in size during this loop.
            index_t quad = local.look_up_quads[i];

            // Walk N to corresponding look S flag is reached.
            quad = find_look_S(quad);

            // Only 3 possible types of hole start: START_E, START_HOLE_N or
            // START_CORNER for SW corner.
            if (START_E(quad)) {
                Location location(quad, -1, -_nx, Z_NE > 0, false);
                closed_line(location, Hole, local);
            }
            else if (START_HOLE_N(quad)) {
                Location location(quad, -1, -_nx, false, true);
                closed_line(location, Hole, local);
            }
            else {
                assert(START_CORNER(quad) && EXISTS_SW_CORNER(quad));
                Location location(quad, _nx-1, -_nx-1, false, true);
                closed_line(location, Hole, local);
            }
        }
    }
}

template <typename Derived>
FillType BaseContourGenerator<Derived>::default_fill_type()
{
    FillType fill_type = FillType::OuterCodes;
    assert(supports_fill_type(fill_type));
    return fill_type;
}

template <typename Derived>
LineType BaseContourGenerator<Derived>::default_line_type()
{
    LineType line_type = LineType::SeparateCodes;
    assert(supports_line_type(line_type));
    return line_type;
}

template <typename Derived>
void BaseContourGenerator<Derived>::export_filled(
    ChunkLocal& local, const std::vector<double>& all_points, std::vector<py::list>& return_lists)
{
    // all_points is only used for fill_types OuterCodes and OuterOffsets.

    typename Derived::Lock lock(static_cast<Derived&>(*this));

    switch (_fill_type)
    {
        case FillType::OuterCodes:
        case FillType::OuterOffsets:
            if (local.total_point_count > 0) {
                auto outer_count = local.line_count - local.hole_count;
                for (decltype(outer_count) i = 0; i < outer_count; ++i) {
                    auto outer_start = local.outer_offsets[i];
                    auto outer_end = local.outer_offsets[i+1];
                    auto point_start = local.line_offsets[outer_start];
                    auto point_end = local.line_offsets[outer_end];
                    auto point_count = point_end - point_start;
                    assert(point_count > 2);

                    return_lists[0].append(Converter::convert_points(
                        point_count, all_points.data() + 2*point_start));

                    if (_fill_type == FillType::OuterCodes)
                        return_lists[1].append(Converter::convert_codes(
                            point_count, outer_end - outer_start + 1,
                            local.line_offsets.data() + outer_start, point_start));
                    else
                        return_lists[1].append(Converter::convert_offsets(
                            outer_end - outer_start + 1, local.line_offsets.data() + outer_start,
                            point_start));
                }
            }
            break;
        case FillType::ChunkCombinedCodes:
        case FillType::ChunkCombinedCodesOffsets:
            if (local.total_point_count > 0) {
                // return_lists[0] already set.
                assert(!local.line_offsets.empty());
                return_lists[1][local.chunk] = Converter::convert_codes(
                    local.total_point_count, local.line_offsets.size(), local.line_offsets.data());

                if (_fill_type == FillType::ChunkCombinedCodesOffsets)
                    return_lists[2][local.chunk] =
                        Converter::convert_offsets_nested(
                            local.outer_offsets.size(), local.outer_offsets.data(),
                            local.line_offsets.data());
            }
            else {
                for (auto& list : return_lists)
                    list[local.chunk] = py::none();
            }
            break;
        case FillType::ChunkCombinedOffsets:
        case FillType::ChunkCombinedOffsets2:
            if (local.total_point_count > 0) {
                // return_lists[0] already set.
                assert(!local.line_offsets.empty());
                return_lists[1][local.chunk] = Converter::convert_offsets(
                    local.line_offsets.size(), local.line_offsets.data());

                if (_fill_type == FillType::ChunkCombinedOffsets2)
                    return_lists[2][local.chunk] = Converter::convert_offsets(
                        local.outer_offsets.size(), local.outer_offsets.data());
            }
            else {
                for (auto& list : return_lists)
                    list[local.chunk] = py::none();
            }
            break;
    }
}

template <typename Derived>
void BaseContourGenerator<Derived>::export_lines(
    ChunkLocal& local, const double* all_points_ptr, std::vector<py::list>& return_lists)
{
    typename Derived::Lock lock(static_cast<Derived&>(*this));

    switch (_line_type)
    {
        case LineType::Separate:
        case LineType::SeparateCodes:
            if (local.total_point_count > 0) {
                assert(all_points_ptr != nullptr);
                for (size_t i = 0; i < local.line_count; ++i) {
                    auto point_start = local.line_offsets[i];
                    auto point_end = local.line_offsets[i+1];
                    auto point_count = point_end - point_start;
                    assert(point_count > 1);

                    return_lists[0].append(Converter::convert_points(
                        point_count, all_points_ptr + 2*point_start));

                    if (_line_type == LineType::SeparateCodes) {
                        return_lists[1].append(
                            Converter::convert_codes_check_closed_single(
                                point_count, all_points_ptr + 2*point_start));
                    }
                }
            }
            break;
        case LineType::ChunkCombinedCodes: {
            if (local.total_point_count > 0) {
                // return_lists[0] already set.
                assert(all_points_ptr != nullptr);
                assert(!local.line_offsets.empty());
                return_lists[1][local.chunk] =
                    Converter::convert_codes_check_closed(
                        local.total_point_count, local.line_offsets.size(),
                        local.line_offsets.data(), all_points_ptr);
            }
            else {
                for (auto& list : return_lists)
                    list[local.chunk] = py::none();
            }
            break;
        }
        case LineType::ChunkCombinedOffsets:
            if (local.total_point_count > 0) {
                // return_lists[0] already set.
                assert(!local.line_offsets.empty());
                return_lists[1][local.chunk] = Converter::convert_offsets(
                    local.line_offsets.size(), local.line_offsets.data());
            }
            else {
                for (auto& list : return_lists)
                    list[local.chunk] = py::none();
            }
            break;
    }
}

template <typename Derived>
py::sequence BaseContourGenerator<Derived>::filled(
    const double& lower_level, const double& upper_level)
{
    if (lower_level > upper_level)
        throw std::invalid_argument("upper and lower levels are the wrong way round");

    _filled = true;
    _lower_level = lower_level;
    _upper_level = upper_level;
    _identify_holes = (_fill_type != FillType::ChunkCombinedCodes &&
                       _fill_type != FillType::ChunkCombinedOffsets);
    _return_list_count = (_fill_type == FillType::ChunkCombinedCodesOffsets ||
                          _fill_type == FillType::ChunkCombinedOffsets2) ? 3 : 2;

    return static_cast<Derived*>(this)->march_wrapper();
}

template <typename Derived>
index_t BaseContourGenerator<Derived>::find_look_S(index_t look_N_quad) const
{
    assert(_identify_holes);

    // Might need to be careful when looking in the same quad as the LOOK_UP.
    index_t quad = look_N_quad;

    // look_S quad must have 1 of only 3 possible types of hole start (START_E,
    // START_HOLE_N, START_CORNER for SW corner) but it may have other starts
    // as well.

    // Start quad may be both a look_N and look_S quad.  Only want to stop
    // search here if look_S hole start is N of look_N.

    if (!LOOK_S(quad)) {
        do
        {
            quad += _nx;
            assert(quad >= 0 && quad < _n);
            assert(EXISTS_ANY(quad));
        } while (!LOOK_S(quad));
    }

    return quad;
}

template <typename Derived>
bool BaseContourGenerator<Derived>::follow_boundary(
    Location& location, const Location& start_location, ChunkLocal& local, size_t& point_count)
{
    // forward values for boundaries:
    //     -1 = N boundary, E to W.
    //      1 = S boundary, W to E.
    //   -_nx = W boundary, N to S.
    //    _nx = E boundary, S to N.
    // -_nx+1 = NE corner, NW to SE.
    //  _nx+1 = NW corner, SW to NE.
    // -_nx-1 = SE corner, NE to SW.
    //  _nx-1 = SW corner, SE to NW.

    assert(is_quad_in_chunk(start_location.quad, local));
    assert(is_quad_in_chunk(location.quad, local));

    // Local variables for faster access.
    auto quad = location.quad;
    auto forward = location.forward;
    auto left = location.left;
    auto start_quad = start_location.quad;
    auto start_forward = start_location.forward;
    auto start_left = start_location.left;
    auto pass = local.pass;

    index_t start_point = 0;
    if (forward > 0) {
        if (forward == _nx) {
            assert(left == -1);
            start_point = quad-_nx;
        }
        else if (left == _nx) {
            assert(forward == 1);
            start_point = quad-_nx-1;
        }
        else if (EXISTS_SW_CORNER(quad)) {
            assert(forward == _nx-1 && left == -_nx-1);
            start_point = quad-_nx;
        }
        else {
            assert(EXISTS_NW_CORNER(quad) && forward == _nx+1 && left == _nx-1);
            start_point = quad-_nx-1;
        }
    }
    else if (forward < 0) {
        if (forward == -_nx) {
            assert(left == 1);
            start_point = quad-1;
        }
        else if (left == -_nx) {
            assert(forward == -1);
            start_point = quad;
        }
        else if (EXISTS_NE_CORNER(quad)) {
            assert(forward == -_nx+1 && left == _nx+1);
            start_point = quad-1;
        }
        else {
            assert(EXISTS_SE_CORNER(quad) && forward == -_nx-1 && left == -_nx+1);
            start_point = quad;
        }
    }

    auto end_point = start_point + forward;

    assert(is_point_in_chunk(start_point, local));
    assert(is_point_in_chunk(end_point, local));

    auto start_z = Z_LEVEL(start_point);
    auto end_z = Z_LEVEL(end_point);

    // Add new point, somewhere along start line.  May be at start point of edge
    // if this is a boundary start.
    point_count++;
    if (pass > 0) {
        if (start_z == 1)
            get_point_xy(start_point, local.points);
        else  // start_z != 1
            interp(start_point, end_point, location.is_upper, local);
    }

    bool finished = false;
    while (true) {
        assert(is_quad_in_chunk(quad, local));

        if (quad == start_quad && forward == start_forward && left == start_left) {
            if (start_location.on_boundary && point_count > 1) {
                // Polygon closed.
                finished = true;
                break;
            }
        }
        else if (pass == 0) {
            // Clear unwanted start locations.
            if (left == _nx) {
                if (START_BOUNDARY_S(quad)) {
                    assert(forward == 1);
                    _cache[quad] &= ~MASK_START_BOUNDARY_S;
                }
            }
            else if (forward == -_nx) {
                if (START_BOUNDARY_W(quad)) {
                    assert(left == 1);
                    _cache[quad] &= ~MASK_START_BOUNDARY_W;
                }
            }
            else if (left == -_nx) {
                if (START_HOLE_N(quad)) {
                    assert(forward == -1);
                    _cache[quad] &= ~MASK_START_HOLE_N;
                }
            }
            else {
                switch (EXISTS_ANY_CORNER(quad)) {
                    case MASK_EXISTS_NE_CORNER:
                        if (left == _nx+1) {
                            assert(forward == -_nx+1);
                            _cache[quad] &= ~MASK_START_CORNER;
                        }
                        break;
                    case MASK_EXISTS_NW_CORNER:
                        if (forward == _nx+1) {
                            assert(left == _nx-1);
                            _cache[quad] &= ~MASK_START_CORNER;
                        }
                        break;
                    case MASK_EXISTS_SE_CORNER:
                        if (forward == -_nx-1) {
                            assert(left == -_nx+1);
                            _cache[quad] &= ~MASK_START_CORNER;
                        }
                        break;
                    case MASK_EXISTS_SW_CORNER:
                        if (left == -_nx-1) {
                            assert(forward == _nx-1);
                            _cache[quad] &= ~MASK_START_CORNER;
                        }
                        break;
                    default:
                        assert(!EXISTS_ANY_CORNER(quad));
                        break;
                }
            }
        }

        // Check if need to leave boundary into interior.
        if (end_z != 1) {
            location.is_upper = (end_z == 2);  // Leave via this level.
            auto temp = forward;
            forward = left;
            left = -temp;
            break;
        }

        // Add end point.
        point_count++;
        if (pass > 0) {
            get_point_xy(end_point, local.points);

            if (LOOK_N(quad) && _identify_holes &&
                (left == _nx || left == _nx+1 || forward == _nx+1)) {
                assert(BOUNDARY_N(quad-_nx) || EXISTS_NE_CORNER(quad) || EXISTS_NW_CORNER(quad));
                local.look_up_quads.push_back(quad);
            }
        }

        move_to_next_boundary_edge(quad, forward, left);

        start_point = end_point;
        start_z = end_z;
        end_point = start_point + forward;
        end_z = Z_LEVEL(end_point);
    }

    location.quad = quad;
    location.forward = forward;
    location.left = left;

    return finished;
}

template <typename Derived>
bool BaseContourGenerator<Derived>::follow_interior(
    Location& location, const Location& start_location, ChunkLocal& local, size_t& point_count)
{
    // Adds the start point in each quad visited, but not the end point unless closing the polygon.
    // Only need to consider a single level of course.
    assert(is_quad_in_chunk(start_location.quad, local));
    assert(is_quad_in_chunk(location.quad, local));

    // Local variables for faster access.
    auto quad = location.quad;
    auto forward = location.forward;
    auto left = location.left;
    auto is_upper = location.is_upper;
    auto start_quad = start_location.quad;
    auto start_forward = start_location.forward;
    auto start_left = start_location.left;
    auto pass = local.pass;

    // left direction, and indices of points on entry edge.
    index_t left_point = 0;
    bool start_corner_diagonal = false;
    if (forward > 0) {
        if (forward == _nx) {
            assert(left == -1);
            left_point = quad-_nx-1;
        }
        else if (left == _nx) {
            assert(forward == 1);
            left_point = quad-1;
        }
        else if (EXISTS_NW_CORNER(quad)) {
            assert(forward == _nx-1 && left == -_nx-1);
            left_point = quad-_nx-1;
            start_corner_diagonal = true;
        }
        else {
            assert(EXISTS_NE_CORNER(quad) && forward == _nx+1 && left == _nx-1);
            left_point = quad-1;
            start_corner_diagonal = true;
        }
    }
    else {  // forward < 0
        if (forward == -_nx) {
            assert(left == 1);
            left_point = quad;
        }
        else if (left == -_nx) {
            assert(forward == -1);
            left_point = quad-_nx;
        }
        else if (EXISTS_SW_CORNER(quad)) {
            assert(forward == -_nx-1 && left == -_nx+1);
            left_point = quad-_nx;
            start_corner_diagonal = true;
        }
        else {
            assert(EXISTS_SE_CORNER(quad) && forward == -_nx+1 && left == _nx+1);
            left_point = quad;
            start_corner_diagonal = true;
        }
    }

    auto right_point = left_point - left;
    bool want_look_N = _identify_holes && pass > 0;

    bool finished = false;  // Whether finished line, i.e. returned to start.
    while (true) {
        assert(is_quad_in_chunk(quad, local));
        assert(is_point_in_chunk(left_point, local));
        assert(is_point_in_chunk(right_point, local));

        if (pass > 0)
            interp(left_point, right_point, is_upper, local);
        point_count++;

        if (quad == start_quad && forward == start_forward &&
            left == start_left && is_upper == start_location.is_upper &&
            !start_location.on_boundary && point_count > 1) {
            finished = true;  // Polygon closed, exit immediately.
            break;
        }

        // Indices of the opposite points.
        auto opposite_left_point = left_point + forward;
        auto opposite_right_point = right_point + forward;
        bool corner_opposite_is_right = false;  // Only used for corners.

        if (start_corner_diagonal) {
            // To avoid dealing with diagonal forward and left below, switch to
            // direction 45 degrees to left, e.g. NW corner faces west using
            // forward == -1.
            corner_opposite_is_right = true;
            switch (EXISTS_ANY_CORNER(quad)) {
                case MASK_EXISTS_NW_CORNER:
                    forward = -1;
                    left = -_nx;
                    opposite_left_point = opposite_right_point = quad-1;
                    break;
                case MASK_EXISTS_NE_CORNER:
                    forward = _nx;
                    left = -1;
                    opposite_left_point = opposite_right_point = quad;
                    break;
                case MASK_EXISTS_SW_CORNER:
                    forward = -_nx;
                    left = 1;
                    opposite_left_point = opposite_right_point = quad-_nx-1;
                    break;
                default:
                    assert(EXISTS_SE_CORNER(quad));
                    forward = 1;
                    left = _nx;
                    opposite_left_point = opposite_right_point = quad-_nx;
                    break;
            }
        }

        // z-levels of the opposite points.
        ZLevel z_opposite_left = Z_LEVEL(opposite_left_point);
        ZLevel z_opposite_right = Z_LEVEL(opposite_right_point);

        int turn_left = -1;  // 1 is turn left, 0 move forward, -1 turn right.
        ZLevel z_test = is_upper ? 2 : 0;

        if (EXISTS_QUAD(quad)) {
            if (z_opposite_left == z_test) {
                if (z_opposite_right == z_test || SADDLE_Z_LEVEL(quad) == z_test)
                    turn_left = 1;
            }
            else if (z_opposite_right == z_test)
                turn_left = 0;
        }
        else if (start_corner_diagonal) {
            turn_left = z_opposite_left == z_test ? 0 : -1;
        }
        else {
            switch (EXISTS_ANY_CORNER(quad)) {
                case MASK_EXISTS_NW_CORNER:
                    corner_opposite_is_right = forward == -_nx;
                    break;
                case MASK_EXISTS_NE_CORNER:
                    corner_opposite_is_right = forward == -1;
                    break;
                case MASK_EXISTS_SW_CORNER:
                    corner_opposite_is_right = forward == 1;
                    break;
                default:
                    assert(EXISTS_SE_CORNER(quad));
                    corner_opposite_is_right = forward == _nx;
                    break;
            }

            if (corner_opposite_is_right)
                turn_left = z_opposite_right == z_test ? 0 : -1;
            else
                turn_left = z_opposite_left == z_test ? 1 : 0;
        }

        // Clear unwanted start locations.
        if (pass == 0 && !(quad == start_quad && forward == start_forward && left == start_left)) {
            if (START_E(quad) && forward == -1 && left == -_nx && turn_left == -1 &&
                (is_upper ? Z_NE > 0 : Z_NE < 2)) {
                _cache[quad] &= ~MASK_START_E;  // E high if is_upper else low.

                if (!_filled && quad < start_location.quad)
                    // Already counted points from here onwards.
                    break;
            }
            else if (START_N(quad) && forward == -_nx && left == 1 && turn_left == 1 &&
                     (is_upper ? Z_NW > 0 : Z_NW < 2)) {
                _cache[quad] &= ~MASK_START_N;  // E high if is_upper else low.

                if (!_filled && quad < start_location.quad)
                    // Already counted points from here onwards.
                    break;
            }
        }

        bool reached_boundary = false;

        // Determine entry edge and left and right points of next quad.
        // Do not update quad index yet.
        if (turn_left > 0) {
            auto temp = forward;
            forward = left;
            left = -temp;
            // left_point unchanged.
            right_point = opposite_left_point;
        }
        else if (turn_left < 0) {  // turn right
            auto temp = forward;
            forward = -left;
            left = temp;
            left_point = opposite_right_point;
            // right_point unchanged.
        }
        else if (EXISTS_QUAD(quad)) {  // Straight on in quad.
            // forward and left stay the same.
            left_point = opposite_left_point;
            right_point = opposite_right_point;
        }
        else if (start_corner_diagonal) {  // Straight on diagonal start corner.
            // left point unchanged.
            right_point = opposite_right_point;
        }
        else {  // Straight on in a corner reaches boundary.
            assert(EXISTS_ANY_CORNER(quad));
            reached_boundary = true;

            if (corner_opposite_is_right) {
                // left_point unchanged.
                right_point = opposite_right_point;
            }
            else {
                left_point = opposite_left_point;
                // right_point unchanged.
            }

            // Set forward and left for correct exit along boundary.
            switch (EXISTS_ANY_CORNER(quad)) {
                case MASK_EXISTS_NW_CORNER:
                    forward = _nx+1;
                    left = _nx-1;
                    break;
                case MASK_EXISTS_NE_CORNER:
                    forward = -_nx+1;
                    left = _nx+1;
                    break;
                case MASK_EXISTS_SW_CORNER:
                    forward = _nx-1;
                    left = -_nx-1;
                    break;
                default:
                    assert(EXISTS_SE_CORNER(quad));
                    forward = -_nx-1;
                    left = -_nx+1;
                    break;
            }
        }

        if (want_look_N && LOOK_N(quad) && forward == 1) {
            // Only consider look_N if pass across E edge of this quad.
            // Care needed if both look_N and look_S set in quad because this
            // line corresponds to only one of them, so want to ignore the
            // look_N if it is the other line otherwise it will be double
            // counted.
            if (!LOOK_S(quad) || (is_upper ? Z_NE < 2 : Z_NE > 0))
                local.look_up_quads.push_back(quad);
        }

        // Check if reached NSEW boundary; already checked and noted if reached
        // corner boundary.
        if (!reached_boundary) {
            if (forward > 0) {
                if (forward == 1)
                    reached_boundary = BOUNDARY_E(quad);
                else
                    reached_boundary = BOUNDARY_N(quad);
            }
            else {  // forward < 0
                if (forward == -1)
                    reached_boundary = BOUNDARY_W(quad);
                else
                    reached_boundary = BOUNDARY_S(quad);
            }

            if (reached_boundary) {
                auto temp = forward;
                forward = left;
                left = -temp;
            }
        }

        // If reached a boundary, return.
        if (reached_boundary) {
            if (!_filled) {
                point_count++;
                if (pass > 0)
                    interp(left_point, right_point, false, local);
            }
            break;
        }

        quad += forward;
        start_corner_diagonal = false;
    }

    location.quad = quad;
    location.forward = forward;
    location.left = left;
    location.is_upper = is_upper;

    return finished;
}

template <typename Derived>
py::tuple BaseContourGenerator<Derived>::get_chunk_count() const
{
    return py::make_tuple(_ny_chunks, _nx_chunks);
}

template <typename Derived>
void BaseContourGenerator<Derived>::get_chunk_limits(index_t chunk, ChunkLocal& local) const
{
    assert(chunk >= 0 && chunk < _n_chunks && "chunk index out of bounds");

    local.chunk = chunk;

    auto ichunk = chunk % _nx_chunks;
    auto jchunk = chunk / _nx_chunks;

    local.istart = ichunk*_x_chunk_size + 1;
    local.iend = (ichunk < _nx_chunks-1 ? (ichunk+1)*_x_chunk_size : _nx-1);

    local.jstart = jchunk*_y_chunk_size + 1;
    local.jend = (jchunk < _ny_chunks-1 ? (jchunk+1)*_y_chunk_size : _ny-1);
}

template <typename Derived>
py::tuple BaseContourGenerator<Derived>::get_chunk_size() const
{
    return py::make_tuple(_y_chunk_size, _x_chunk_size);
}

template <typename Derived>
bool BaseContourGenerator<Derived>::get_corner_mask() const
{
    return _corner_mask;
}

template <typename Derived>
FillType BaseContourGenerator<Derived>::get_fill_type() const
{
    return _fill_type;
}

template <typename Derived>
LineType BaseContourGenerator<Derived>::get_line_type() const
{
    return _line_type;
}

template <typename Derived>
index_t BaseContourGenerator<Derived>::get_n_chunks() const
{
    return _n_chunks;
}

template <typename Derived>
void BaseContourGenerator<Derived>::get_point_xy(index_t point, double*& points) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    *points++ = _x.data()[point];
    *points++ = _y.data()[point];
}

template <typename Derived>
const double& BaseContourGenerator<Derived>::get_point_x(index_t point) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    return _x.data()[point];
}

template <typename Derived>
const double& BaseContourGenerator<Derived>::get_point_y(index_t point) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    return _y.data()[point];
}

template <typename Derived>
const double& BaseContourGenerator<Derived>::get_point_z(index_t point) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    return _z.data()[point];
}

template <typename Derived>
void BaseContourGenerator<Derived>::init_cache_grid(const MaskArray& mask)
{
    index_t i, j, quad;
    if (mask.ndim() == 0) {
        // No mask, easy to calculate quad existence and boundaries together.
        for (j = 0, quad = 0; j < _ny; ++j) {
            for (i = 0; i < _nx; ++i, ++quad) {
                _cache[quad] = 0;

                if (i > 0 && j > 0)
                    _cache[quad] |= MASK_EXISTS_QUAD;

                if ((i % _x_chunk_size == 0 || i == _nx-1) && j > 0)
                    _cache[quad] |= MASK_BOUNDARY_E;

                if ((j % _y_chunk_size == 0 || j == _ny-1) && i > 0)
                    _cache[quad] |= MASK_BOUNDARY_N;
            }
        }
    }
    else {
        // Could maybe speed this up and just have a single pass.
        // Care would be needed with lookback of course.
        const bool* mask_ptr = mask.data();

        // Have mask so use two stages.
        // Stage 1, determine if quads/corners exist.
        quad = 0;
        for (j = 0; j < _ny; ++j) {
            for (i = 0; i < _nx; ++i, ++quad) {
                _cache[quad] = 0;

                if (i > 0 && j > 0) {
                    unsigned int config = (mask_ptr[POINT_NW] << 3) |
                                          (mask_ptr[POINT_NE] << 2) |
                                          (mask_ptr[POINT_SW] << 1) |
                                          (mask_ptr[POINT_SE] << 0);
                    if (_corner_mask) {
                         switch (config) {
                            case 0: _cache[quad] = MASK_EXISTS_QUAD; break;
                            case 1: _cache[quad] = MASK_EXISTS_NW_CORNER; break;
                            case 2: _cache[quad] = MASK_EXISTS_NE_CORNER; break;
                            case 4: _cache[quad] = MASK_EXISTS_SW_CORNER; break;
                            case 8: _cache[quad] = MASK_EXISTS_SE_CORNER; break;
                            default:
                                // Do nothing, quad is masked out.
                                break;
                        }
                    }
                    else if (config == 0)
                        _cache[quad] = MASK_EXISTS_QUAD;
                }
            }
        }

        // Stage 2, calculate N and E boundaries.
        quad = 0;
        for (j = 0; j < _ny; ++j) {
            bool j_chunk_boundary = j % _y_chunk_size == 0;

            for (i = 0; i < _nx; ++i, ++quad) {
                bool i_chunk_boundary = i % _x_chunk_size == 0;

                if (_corner_mask) {
                    bool exists_E_edge = EXISTS_E_EDGE(quad);
                    bool E_exists_W_edge = (i < _nx-1 && EXISTS_W_EDGE(quad+1));
                    bool exists_N_edge = EXISTS_N_EDGE(quad);
                    bool N_exists_S_edge = (j < _ny-1 && EXISTS_S_EDGE(quad+_nx));

                    if (exists_E_edge != E_exists_W_edge ||
                        (i_chunk_boundary && exists_E_edge && E_exists_W_edge))
                        _cache[quad] |= MASK_BOUNDARY_E;

                    if (exists_N_edge != N_exists_S_edge ||
                        (j_chunk_boundary && exists_N_edge && N_exists_S_edge))
                         _cache[quad] |= MASK_BOUNDARY_N;
                }
                else {
                    bool E_exists_quad = (i < _nx-1 && EXISTS_QUAD(quad+1));
                    bool N_exists_quad = (j < _ny-1 && EXISTS_QUAD(quad+_nx));
                    bool exists = EXISTS_QUAD(quad);

                    if (exists != E_exists_quad || (i_chunk_boundary && exists && E_exists_quad))
                        _cache[quad] |= MASK_BOUNDARY_E;

                    if (exists != N_exists_quad || (j_chunk_boundary && exists && N_exists_quad))
                        _cache[quad] |= MASK_BOUNDARY_N;
                }
            }
        }
    }
}

template <typename Derived>
void BaseContourGenerator<Derived>::init_cache_levels_and_starts(
    const ChunkLocal& local, bool ordered_chunks)
{
    CacheItem keep_mask =
        (_corner_mask ? MASK_EXISTS_ANY | MASK_BOUNDARY_N | MASK_BOUNDARY_E
                      : MASK_EXISTS_QUAD | MASK_BOUNDARY_N | MASK_BOUNDARY_E);

    index_t istart = local.istart > 1 ? local.istart : 0;
    index_t iend = local.iend;
    index_t jstart = local.jstart > 1 ? local.jstart : 0;
    index_t jend = local.jend;

    index_t j_final_start = jstart - 1;

    for (index_t j = jstart; j <= jend; ++j) {
        index_t quad = istart + j*_nx;
        const double* z_ptr = _z.data() + quad;
        bool start_in_row = false;

        // z-level of NW point not needed if i == 0, otherwise read it from cache as already
        // calculated.  Do not read if from cache if !ordered_chunks and it is in another chunk as
        // it may not have been set yet, so calculate it now for temporary use.
        ZLevel z_nw = (istart == 0) ? 0 :
            ((!ordered_chunks && istart == local.istart && istart > 1) ?
                z_to_zlevel(*(z_ptr-1)) : Z_NW);

        // z-level of SW point not needed if i == 0 or j == 0, otherwise read it from cache as
        // already calculated.  Do not read it from cache if !ordered_chunks and it is in another
        // chunk as it may not have been set yet, so calculate it now for temporary use.
        ZLevel z_sw = (istart == 0 || j == 0) ? 0 :
            ((!ordered_chunks && (j == jstart || (istart == local.istart && istart > 1))) ?
                z_to_zlevel(*(z_ptr-_nx-1)) : Z_SW);

        for (index_t i = istart; i <= iend; ++i, ++quad, ++z_ptr) {
            // z-level of SE point not needed if j == 0, otherwise read it from cache as already
            // calculated.  Do not read it from cache if !ordered_chunks and it is in another chunk
            // as it may have not been set yet, so calculate it now for temporary use.
            ZLevel z_se = (j == 0) ? 0 :
                ((!ordered_chunks && j == jstart) ? z_to_zlevel(*(z_ptr-_nx)) : Z_SE);

            _cache[quad] &= keep_mask;
            _cache[quad] |= MASK_SADDLE;

            // Cache z-level of NE point.
            ZLevel z_ne = 0;
            if (_filled && *z_ptr > _upper_level) {
                _cache[quad] |= MASK_Z_LEVEL_2;
                z_ne = 2;
            }
            else if (*z_ptr > _lower_level) {
                _cache[quad] |= MASK_Z_LEVEL_1;
                z_ne = 1;
            }

            if (EXISTS_ANY(quad)) {
                if (_filled) {
                    if (EXISTS_N_AND_E_EDGES(quad)) {
                        if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw == 0 || SADDLE_Z_LEVEL(quad) == 0)) {
                            _cache[quad] |= MASK_START_N;  // N to E low.
                        }
                        else if (z_nw == 2 && z_se == 2 && z_ne < 2 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw == 2 ||
                                  SADDLE_Z_LEVEL(quad) == 2)) {
                            _cache[quad] |= MASK_START_N;  // N to E high.
                        }

                        if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                            _cache[quad] |= MASK_START_E;  // E to N low.
                        }
                        else if (z_ne == 2 && z_nw < 2 && z_se < 2 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw < 2 || SADDLE_Z_LEVEL(quad) < 2)) {
                            _cache[quad] |= MASK_START_E;  // E to N high.
                        }
                    }

                    if (BOUNDARY_S(quad) &&
                        ((z_sw == 2 && z_se < 2) || (z_sw == 0 && z_se > 0) || z_sw == 1)) {
                        _cache[quad] |= MASK_START_BOUNDARY_S;
                    }

                    if (BOUNDARY_W(quad) &&
                        ((z_nw == 2 && z_sw < 2) || (z_nw == 0 && z_sw > 0) ||
                         (z_nw == 1 && (z_sw != 1 || EXISTS_NW_CORNER(quad))))) {
                        _cache[quad] |= MASK_START_BOUNDARY_W;
                    }

                    if (EXISTS_ANY_CORNER(quad)) {
                        if (EXISTS_NE_CORNER(quad) &&
                            ((z_nw == 2 && z_se < 2) || (z_nw == 0 && z_se > 0) || z_nw == 1)) {
                            _cache[quad] |= MASK_START_CORNER;
                        }
                        else if (EXISTS_NW_CORNER(quad) &&
                                 ((z_sw == 2 && z_ne < 2) || (z_sw == 0 && z_ne > 0))) {
                            _cache[quad] |= MASK_START_CORNER;
                        }
                        else if (EXISTS_SE_CORNER(quad) && ((z_sw == 0 && z_se == 0 && z_ne > 0) ||
                                                            (z_sw == 2 && z_se == 2 && z_ne < 2))) {
                            _cache[quad] |= MASK_START_CORNER;
                        }
                        else if (EXISTS_SW_CORNER(quad) && z_nw == 1 && z_se == 1) {
                            _cache[quad] |= MASK_START_CORNER;
                        }
                    }

                    // Start following N boundary from E to W which is a hole.
                    // Required for an internal masked region which is a hole in
                    // a filled polygon.
                    if (BOUNDARY_N(quad) && EXISTS_N_EDGE(quad) && z_nw == 1 && z_ne == 1 &&
                        !START_HOLE_N(quad-1) && j % _y_chunk_size != 0 && j != _ny-1) {
                        _cache[quad] |= MASK_START_HOLE_N;
                    }

                    start_in_row |= ANY_START_FILLED(quad);
                }
                else {  // !_filled
                    if (BOUNDARY_S(quad) && z_sw == 1 && z_se == 0)
                        _cache[quad] |= MASK_START_BOUNDARY_S;

                    if (BOUNDARY_W(quad) && z_nw == 1 && z_sw == 0)
                        _cache[quad] |= MASK_START_BOUNDARY_W;

                    if (BOUNDARY_E(quad) && z_se == 1 && z_ne == 0)
                        _cache[quad] |= MASK_START_BOUNDARY_E;

                    if (BOUNDARY_N(quad) && z_ne == 1 && z_nw == 0)
                        _cache[quad] |= MASK_START_BOUNDARY_N;

                    if (EXISTS_N_AND_E_EDGES(quad) && !BOUNDARY_N(quad) && !BOUNDARY_E(quad)) {
                        if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                            _cache[quad] |= MASK_START_E;  // E to N low.
                        }
                        else if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw == 0 ||
                                  SADDLE_Z_LEVEL(quad) == 0)) {
                            _cache[quad] |= MASK_START_N;  // N to E low.
                        }
                    }

                    if (EXISTS_ANY_CORNER(quad)) {
                        bool corner_start = false;
                        if (EXISTS_NW_CORNER(quad))
                            corner_start = (z_sw == 1 && z_ne == 0);
                        else if (EXISTS_NE_CORNER(quad))
                            corner_start = (z_nw == 1 && z_se == 0);
                        else if (EXISTS_SW_CORNER(quad))
                            corner_start = (z_se == 1 && z_nw == 0);
                        else  // EXISTS_SE_CORNER
                            corner_start = (z_ne == 1 && z_sw == 0);

                        if (corner_start)
                           _cache[quad] |= MASK_START_CORNER;
                    }

                    start_in_row |= ANY_START_LINES(quad);
                }
            } // EXISTS_ANY(quad)

            z_nw = z_ne;
            z_sw = z_se;
        } // i-loop.

        if (start_in_row)
            j_final_start = j;
        else if (j > 0)
            _cache[local.istart + j*_nx] |= MASK_NO_STARTS_IN_ROW;
    } // j-loop.

    if (j_final_start < local.jend) {
        //std::cout << "NO MORE STARTS j_final_start=" << j_final_start
          //  << " quad=" << local.istart + (j_final_start+1)*_nx << std::endl;
        _cache[local.istart + (j_final_start+1)*_nx] |= MASK_NO_MORE_STARTS;
    }
}

template <typename Derived>
void BaseContourGenerator<Derived>::interp(
    index_t point0, index_t point1, bool is_upper, ChunkLocal& local) const
{
    assert(is_point_in_chunk(point0, local));
    assert(is_point_in_chunk(point1, local));

    const double& z1 = get_point_z(point1);
    const double& level = is_upper ? _upper_level : _lower_level;

    double frac;
    switch (_interp) {
        case Interp::Log:
            // Equivalent to
            //   (log(z1) - log(level)) / (log(z1) - log(z0))
            // Same result obtained regardless of logarithm base.
            frac = log(z1/level) / log(z1/get_point_z(point0));
            break;
        default:  // Interp::Linear
            frac = (z1 - level) / (z1 - get_point_z(point0));
            break;
    }

    assert(frac >= 0.0 && frac <= 1.0 && "Interp fraction out of bounds");

    *local.points++ = get_point_x(point0)*frac + get_point_x(point1)*(1.0 - frac);
    *local.points++ = get_point_y(point0)*frac + get_point_y(point1)*(1.0 - frac);
}

template <typename Derived>
bool BaseContourGenerator<Derived>::is_filled() const
{
    return _filled;
}

template <typename Derived>
bool BaseContourGenerator<Derived>::is_point_in_chunk(index_t point, const ChunkLocal& local) const
{
    return is_quad_in_bounds(
        point, local.istart-1, local.iend, local.jstart-1, local.jend);
}

template <typename Derived>
bool BaseContourGenerator<Derived>::is_quad_in_bounds(
    index_t quad, index_t istart, index_t iend, index_t jstart, index_t jend) const
{
    return (quad % _nx >= istart && quad % _nx <= iend &&
            quad / _nx >= jstart && quad / _nx <= jend);
}

template <typename Derived>
bool BaseContourGenerator<Derived>::is_quad_in_chunk(index_t quad, const ChunkLocal& local) const
{
    return is_quad_in_bounds(quad, local.istart, local.iend, local.jstart, local.jend);
}

template <typename Derived>
void BaseContourGenerator<Derived>::line(const Location& start_location, ChunkLocal& local)
{
    // start_location.on_boundary indicates starts (and therefore also finishes)

    assert(is_quad_in_chunk(start_location.quad, local));

    Location location = start_location;
    size_t point_count = 0;

    // finished == true indicates closed line loop.
    bool finished = follow_interior(location, start_location, local, point_count);

    if (local.pass > 0)
        local.line_offsets[local.line_count] = local.total_point_count;

    if (local.pass == 0 && !start_location.on_boundary && !finished)
        // An internal start that isn't a line loop is part of a line strip that
        // starts on a boundary and will be traced later.  Do not count it as a
        // valid start in pass 0 and remove the first point or it will be
        // duplicated by the correct boundary-started line later.
        point_count--;
    else
        local.line_count++;

    local.total_point_count += point_count;
}

template <typename Derived>
py::sequence BaseContourGenerator<Derived>::lines(const double& level)
{
    _filled = false;
    _lower_level = _upper_level = level;
    _identify_holes = false;
    _return_list_count = (_line_type == LineType::Separate) ? 1 : 2;

    return static_cast<Derived*>(this)->march_wrapper();
}

template <typename Derived>
void BaseContourGenerator<Derived>::march_chunk_filled(
    ChunkLocal& local, std::vector<py::list>& return_lists)
{
    // Allocated at end of pass 0, depending on _fill_type.
    std::vector<double> all_points;

    for (local.pass = 0; local.pass < 2; ++local.pass) {
        bool ignore_holes = (_identify_holes && local.pass == 1);

        index_t j_final_start = local.jstart;
        for (index_t j = local.jstart; j <= local.jend; ++j) {
            index_t quad = local.istart + j*_nx;

            if (NO_MORE_STARTS(quad))
                break;

            if (NO_STARTS_IN_ROW(quad))
                continue;

            // Want to count number of starts in this row, so store how many
            // starts at start of row.
            size_t prev_start_count =
                (_identify_holes ? local.line_count - local.hole_count : local.line_count);

            for (index_t i = local.istart; i <= local.iend; ++i, ++quad) {
                if (!ANY_START_FILLED(quad))
                    continue;

                assert(EXISTS_ANY(quad));

                if (START_BOUNDARY_S(quad)) {
                    Location location(quad, 1, _nx, Z_SW == 2, true);
                    closed_line_wrapper(location, Outer, local);
                }

                if (START_BOUNDARY_W(quad)) {
                    Location location(quad, -_nx, 1, Z_NW == 2, true);
                    closed_line_wrapper(location, Outer, local);
                }

                if (START_CORNER(quad)) {
                    switch (EXISTS_ANY_CORNER(quad)) {
                        case MASK_EXISTS_NE_CORNER: {
                            Location location(quad, -_nx+1, _nx+1, Z_NW == 2, true);
                            closed_line_wrapper(location, Outer, local);
                            break;
                        }
                        case MASK_EXISTS_NW_CORNER: {
                            Location location(quad, _nx+1, _nx-1, Z_SW == 2, true);
                            closed_line_wrapper(location, Outer, local);
                            break;
                        }
                        case MASK_EXISTS_SE_CORNER: {
                            Location location(quad, -_nx-1, -_nx+1, Z_NE == 2, true);
                            closed_line_wrapper(location, Outer, local);
                            break;
                        }
                        default:
                            assert(EXISTS_SW_CORNER(quad));
                            if (!ignore_holes) {
                                Location location(quad, _nx-1, -_nx-1, false, true);
                                closed_line_wrapper(location, Hole, local);
                            }
                            break;
                    }
                }

                if (START_N(quad)) {
                    Location location(quad, -_nx, 1, Z_NW > 0, false);
                    closed_line_wrapper(location, Outer, local);
                }

                if (ignore_holes)
                    continue;

                if (START_E(quad)) {
                    Location location(quad, -1, -_nx, Z_NE > 0, false);
                    closed_line_wrapper(location, Hole, local);
                }

                if (START_HOLE_N(quad)) {
                    Location location(quad, -1, -_nx, false, true);
                    closed_line_wrapper(location, Hole, local);
                }
            } // i

            // Number of starts at end of row.
            size_t start_count =
                (_identify_holes ? local.line_count - local.hole_count : local.line_count);
            if (start_count - prev_start_count)
                j_final_start = j;
            else
                _cache[local.istart + j*_nx] |= MASK_NO_STARTS_IN_ROW;
        } // j

        if (j_final_start < local.jend)
            _cache[local.istart + (j_final_start+1)*_nx] |= MASK_NO_MORE_STARTS;

        if (local.pass == 0) {
            if (_fill_type == FillType::OuterCodes || _fill_type == FillType::OuterOffsets) {
                all_points.resize(2*local.total_point_count);

                // Where to store contour points.
                local.points = all_points.data();
            }
            else if (local.total_point_count > 0) {  // Combined points.
                py::size_t points_shape[2] = {local.total_point_count, 2};

                typename Derived::Lock lock(static_cast<Derived&>(*this));
                PointArray py_all_points(points_shape);
                lock.unlock();

                return_lists[0][local.chunk] = py_all_points;

                // Where to store contour points.
                local.points = py_all_points.mutable_data();
            }

            // Allocate space for line_offsets, and set final offsets.
            local.line_offsets.resize(local.line_count + 1);
            local.line_offsets.back() = local.total_point_count;

            // Allocate space for outer_offsets, and set final offsets.
            if (_identify_holes) {
                auto outer_count = local.line_count - local.hole_count;
                local.outer_offsets.resize(outer_count + 1);
                local.outer_offsets.back() = local.line_count;
            }
            else
                local.outer_offsets.resize(0);

            local.total_point_count = 0;
            local.line_count = 0;
            local.hole_count = 0;
        }
    } // pass

    // Check both passes returned same number of points, lines, etc.
    assert(local.line_offsets.size() == local.line_count + 1);
    assert(local.line_offsets.back() == local.total_point_count);

    if (_identify_holes) {
        assert(local.outer_offsets.size() == local.line_count - local.hole_count + 1);
        assert(local.outer_offsets.back() == local.line_count);
    }
    else {
        assert(local.outer_offsets.empty());
    }

    export_filled(local, all_points, return_lists);
}

template <typename Derived>
void BaseContourGenerator<Derived>::march_chunk_lines(
    ChunkLocal& local, std::vector<py::list>& return_lists)
{
    // Allocated at end of pass 0, depending on _line_type.
    std::vector<double> all_points;
    const double* all_points_ptr = nullptr;

    for (local.pass = 0; local.pass < 2; ++local.pass) {
        index_t j_final_start = local.jstart;
        for (index_t j = local.jstart; j <= local.jend; ++j) {
            index_t quad = local.istart + j*_nx;

            if (NO_MORE_STARTS(quad))
                break;

            if (NO_STARTS_IN_ROW(quad))
                continue;

            // Want to count number of starts in this row, so store how many
            // starts at start of row.
            auto prev_start_count = local.line_count;

            for (index_t i = local.istart; i <= local.iend; ++i, ++quad) {
                if (!ANY_START_LINES(quad))
                    continue;

                assert(EXISTS_ANY(quad));

                if (START_BOUNDARY_S(quad)) {
                    Location location(quad, _nx, -1, false, true);
                    line(location, local);
                }

                if (START_BOUNDARY_W(quad)) {
                    Location location(quad, 1, _nx, false, true);
                    line(location, local);
                }

                if (START_BOUNDARY_E(quad)) {
                    Location location(quad, -1, -_nx, false, true);
                    line(location, local);
                }

                if (START_BOUNDARY_N(quad)) {
                    Location location(quad, -_nx, 1, false, true);
                    line(location, local);
                }

                if (START_E(quad)) {
                    Location location(quad, -1, -_nx, false, false);
                    line(location, local);
                }

                if (START_N(quad)) {
                    Location location(quad, -_nx, 1, false, false);
                    line(location, local);
                }

                if (START_CORNER(quad)) {
                    index_t forward, left;
                    if (EXISTS_NW_CORNER(quad)) {
                        forward = _nx-1;
                        left = -_nx-1;
                    }
                    else if (EXISTS_NE_CORNER(quad)) {
                        forward = _nx+1;
                        left = _nx-1;
                    }
                    else if (EXISTS_SW_CORNER(quad)) {
                        forward = -_nx-1;
                        left = -_nx+1;
                    }
                    else {  // EXISTS_SE_CORNER
                        forward = -_nx+1;
                        left = _nx+1;
                    }
                    Location location(quad, forward, left, false, true);
                    line(location, local);
                }
            } // i

            // Number of starts at end of row.
            if (local.line_count - prev_start_count)
                j_final_start = j;
            else
                _cache[local.istart + j*_nx] |= MASK_NO_STARTS_IN_ROW;
        } // j

        if (j_final_start < local.jend)
            _cache[local.istart + (j_final_start+1)*_nx] |= MASK_NO_MORE_STARTS;

        if (local.pass == 0) {
            if (_line_type == LineType::Separate || _line_type == LineType::SeparateCodes) {
                all_points.resize(2*local.total_point_count);

                // Where to store contour points.
                local.points = all_points.data();

                // Needed to check if lines are closed loops or not.
                all_points_ptr = all_points.data();
            }
            else if (local.total_point_count > 0) {  // Combined points.
                py::size_t points_shape[2] = {local.total_point_count, 2};

                typename Derived::Lock lock(static_cast<Derived&>(*this));
                PointArray py_all_points(points_shape);
                lock.unlock();

                return_lists[0][local.chunk] = py_all_points;

                // Where to store contour points.
                local.points = py_all_points.mutable_data();

                // Needed to check if lines are closed loops or not.
                all_points_ptr = py_all_points.data();
            }

            // Allocate space for line_offsets, and set final offsets.
            local.line_offsets.resize(local.line_count + 1);
            local.line_offsets.back() = local.total_point_count;

            local.total_point_count = 0;
            local.line_count = 0;
        }
    } // pass

    // Check both passes returned same number of points, lines, etc.
    assert(local.line_offsets.size() == local.line_count + 1);
    assert(local.line_offsets.back() == local.total_point_count);

    export_lines(local, all_points_ptr, return_lists);
}

template <typename Derived>
py::sequence BaseContourGenerator<Derived>::march_wrapper()
{
    index_t list_len = _n_chunks;
    if ((_filled && (_fill_type == FillType::OuterCodes || _fill_type == FillType::OuterOffsets)) ||
        (!_filled && (_line_type == LineType::Separate || _line_type == LineType::SeparateCodes)))
        list_len = 0;

    // Prepare lists to return to python.
    std::vector<py::list> return_lists;
    return_lists.reserve(_return_list_count);
    for (decltype(_return_list_count) i = 0; i < _return_list_count; ++i)
        return_lists.emplace_back(list_len);

    static_cast<Derived*>(this)->march(return_lists);

    // Return to python objects.
    if (_return_list_count == 1) {
        assert(!_filled && _line_type == LineType::Separate);
        return return_lists[0];
    }
    else if (_return_list_count == 2)
        return py::make_tuple(return_lists[0], return_lists[1]);
    else {
        assert(_return_list_count == 3);
        return py::make_tuple(return_lists[0], return_lists[1], return_lists[2]);
    }
}

template <typename Derived>
void BaseContourGenerator<Derived>::move_to_next_boundary_edge(
    index_t& quad, index_t& forward, index_t& left) const
{
    // edge == 0 for E edge (facing N), forward = +_nx
    //         2 for S edge (facing E), forward = +1
    //         4 for W edge (facing S), forward = -_nx
    //         6 for N edge (facing W), forward = -1
    //         1 for SE edge (NW corner) from SW facing NE, forward = +_nx+1
    //         3 for SW edge (NE corner) from NW facing SE, forward = -_nx+1
    //         5 for NW edge (SE corner) from NE facing SW, forward = -_nx-1
    //         7 for NE edge (SW corner) from SE facing NW, forward = +_nx-1
    int edge = 0;

    // Need index of quad that is the same as the end point, i.e. quad to SW of
    // end point, as it is this point which we need to find the next available
    // boundary of, looking clockwise.
    if (forward > 0) {
        if (forward == _nx) {
            assert(left == -1);
            // W edge facing N, no change to quad or edge.
        }
        else if (left == _nx) {
            assert(forward == 1);
            quad -= _nx;  // S edge facing E.
            edge = 2;
        }
        else if (EXISTS_SW_CORNER(quad)) {
            assert(forward == _nx-1 && left == -_nx-1);
            quad -= 1;
            edge = 7;
        }
        else {
            assert(EXISTS_NW_CORNER(quad) && forward == _nx+1 && _nx-1);
            // quad unchanged.
            edge = 1;
        }
    }
    else {  // forward < 0
        if (forward == -_nx) {
            assert(left == 1);
            quad -= _nx+1;  // W edge facing S.
            edge = 4;
        }
        else if (left == -_nx) {
            assert(forward == -1);
            quad -= 1;  // N edge facing W.
            edge = 6;
        }
        else if (EXISTS_NE_CORNER(quad)) {
            assert(forward == -_nx+1 && left == _nx+1);
            quad -= _nx;
            edge = 3;
        }
        else {
            assert(EXISTS_SE_CORNER(quad) && forward == -_nx-1 && left == -_nx+1);
            quad -= _nx+1;
            edge = 5;
        }
    }

    // If _corner_mask not set, only need to consider odd edge in loop below.
    if (!_corner_mask)
        ++edge;

    while (true) {
        // Look at possible edges that leave NE point of quad.
        // If something is wrong here or in the setup of the boundary flags,
        // can end up with an infinite loop!
        switch (edge) {
            case 0:
                // Is there an edge to follow towards SW?
                if (EXISTS_SE_CORNER(quad)) {  // Equivalent to BOUNDARY_NE.
                    // quad unchanged.
                    forward = -_nx-1;
                    left = -_nx+1;
                    return;
                }
                break;
            case 1:
                // Is there an edge to follow towards W?
                if (BOUNDARY_N(quad)) {
                    // quad unchanged.
                    forward = -1;
                    left = -_nx;
                    return;
                }
                break;
            case 2:
                // Is there an edge to follow towards NW?
                if (EXISTS_SW_CORNER(quad+_nx)) {  // Equivalent to BOUNDARY_NE.
                    quad += _nx;
                    forward = _nx-1;
                    left = -_nx-1;
                    return;
                }
                break;
            case 3:
                // Is there an edge to follow towards N?
                if (BOUNDARY_E(quad+_nx)) {  // Really a BOUNDARY_W check.
                    quad += _nx;
                    forward = _nx;
                    left = -1;
                    return;
                }
                break;
            case 4:
                // Is there an edge to follow towards NE?
                if (EXISTS_NW_CORNER(quad+_nx+1)) {  // Equivalent to BOUNDARY_SE.
                    quad += _nx+1;
                    forward = _nx+1;
                    left = _nx-1;
                    return;
                }
                break;
            case 5:
                // Is there an edge to follow towards E?
                if (BOUNDARY_N(quad+1)) {  // Really a BOUNDARY_S check
                    quad += _nx+1;
                    forward = 1;
                    left = _nx;
                    return;
                }
                break;
            case 6:
                // Is there an edge to follow towards SE?
                if (EXISTS_NE_CORNER(quad+1)) {  // Equivalent to BOUNDARY_SW.
                    quad += 1;
                    forward = -_nx+1;
                    left = _nx+1;
                    return;
                }
                break;
            case 7:
                // Is there an edge to follow towards S?
                if (BOUNDARY_E(quad)) {
                    quad += 1;
                    forward = -_nx;
                    left = 1;
                    return;
                }
                break;
            default:
                assert(0 && "Invalid edge index");
                break;
        }

        edge = _corner_mask ? (edge + 1) % 8 : (edge + 2) % 8;
    }
}

template <typename Derived>
void BaseContourGenerator<Derived>::set_look_flags(index_t hole_start_quad)
{
    assert(_identify_holes);

    // The only possible hole starts are START_E (from E to N) and START_HOLE_N
    // (on N boundary, E to W) and START_CORNER for SW corner (on boundary,
    // SE to NW).
    assert(hole_start_quad >= 0 && hole_start_quad < _n);
    assert(EXISTS_N_EDGE(hole_start_quad) || EXISTS_SW_CORNER(hole_start_quad));
    assert(!LOOK_S(hole_start_quad) && "Look S already set");

    _cache[hole_start_quad] |= MASK_LOOK_S;

    // Walk S until find place to mark corresponding look N.
    auto quad = hole_start_quad;

    while (true) {
        assert(quad >= 0 && quad < _n);
        assert(EXISTS_N_EDGE(quad) || (quad == hole_start_quad && EXISTS_SW_CORNER(quad)));

        if (BOUNDARY_S(quad) || EXISTS_NE_CORNER(quad) || EXISTS_NW_CORNER(quad) || Z_SE != 1) {
            assert(!LOOK_N(quad) && "Look N already set");
            _cache[quad] |= MASK_LOOK_N;
            break;
        }

        quad -= _nx;
    }
}

template <typename Derived>
bool BaseContourGenerator<Derived>::supports_fill_type(FillType fill_type)
{
    switch (fill_type) {
        case FillType::OuterCodes:
        case FillType::OuterOffsets:
        case FillType::ChunkCombinedCodes:
        case FillType::ChunkCombinedOffsets:
        case FillType::ChunkCombinedCodesOffsets:
        case FillType::ChunkCombinedOffsets2:
            return true;
        default:
            return false;
    }
}

template <typename Derived>
bool BaseContourGenerator<Derived>::supports_line_type(LineType line_type)
{
    switch (line_type) {
        case LineType::Separate:
        case LineType::SeparateCodes:
        case LineType::ChunkCombinedCodes:
        case LineType::ChunkCombinedOffsets:
            return true;
        default:
            return false;
    }
}

template <typename Derived>
void BaseContourGenerator<Derived>::write_cache() const
{
    std::cout << "---------- Cache ----------" << std::endl;
    index_t ny = _n / _nx;
    for (index_t j = ny-1; j >= 0; --j) {
        std::cout << "j=" << j << " ";
        for (index_t i = 0; i < _nx; ++i) {
            index_t quad = i + j*_nx;
            write_cache_quad(quad);
        }
        std::cout << std::endl;
    }
    std::cout << "    ";
    for (index_t i = 0; i < _nx; ++i)
        std::cout << "i=" << i << "           ";
    std::cout << std::endl;
    std::cout << "---------------------------" << std::endl;
}

template <typename Derived>
void BaseContourGenerator<Derived>::write_cache_quad(index_t quad) const
{
    assert(quad >= 0 && quad < _n && "quad index out of bounds");
    std::cout << (NO_MORE_STARTS(quad) ? 'x' :
                    (NO_STARTS_IN_ROW(quad) ? 'i' : '.'));
    std::cout << (EXISTS_QUAD(quad) ? "Q_" :
                   (EXISTS_NW_CORNER(quad) ? "NW" :
                     (EXISTS_NE_CORNER(quad) ? "NE" :
                       (EXISTS_SW_CORNER(quad) ? "SW" :
                         (EXISTS_SE_CORNER(quad) ? "SE" : "..")))));
    std::cout << (BOUNDARY_N(quad) && BOUNDARY_E(quad) ? 'b' : (
                    BOUNDARY_N(quad) ? 'n' : (BOUNDARY_E(quad) ? 'e' : '.')));
    std::cout << Z_LEVEL(quad);
    std::cout << ((_cache[quad] & MASK_SADDLE) >> 2);
    std::cout << (START_BOUNDARY_S(quad) ? 's' : '.');
    std::cout << (START_BOUNDARY_W(quad) ? 'w' : '.');
    if (!_filled) {
        std::cout << (START_BOUNDARY_E(quad) ? 'e' : '.');
        std::cout << (START_BOUNDARY_N(quad) ? 'n' : '.');
    }
    std::cout << (START_E(quad) ? 'E' : '.');
    std::cout << (START_N(quad) ? 'N' : '.');
    if (_filled)
        std::cout << (START_HOLE_N(quad) ? 'h' : '.');
    std::cout << (START_CORNER(quad) ? 'c' : '.');
    if (_filled)
        std::cout << (LOOK_N(quad) && LOOK_S(quad) ? 'B' :
            (LOOK_N(quad) ? '^' : (LOOK_S(quad) ? 'v' : '.')));
    std::cout << ' ';
}

template <typename Derived>
typename BaseContourGenerator<Derived>::ZLevel BaseContourGenerator<Derived>::z_to_zlevel(
    const double& z_value)
{
    return (_filled && z_value > _upper_level) ? 2 : (z_value > _lower_level ? 1 : 0);
}

#endif // CONTOURPY_BASE_IMPL_H
