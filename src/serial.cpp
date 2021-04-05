#include "chunk_local.h"
#include "converter.h"
#include "serial.h"
#include <iostream>


// Point indices from current quad index.
#define POINT_SW (quad-_nx-1)
#define POINT_SE (quad-_nx)
#define POINT_NW (quad-1)
#define POINT_NE (quad)


// CacheItem masks, only accessed directly to set.  To read, use accessors
// detailed below.  1 and 2 refer to level indices (lower and upper).
#define MASK_Z_LEVEL_1        0x0001 // z > lower_level.
#define MASK_Z_LEVEL_2        0x0002 // z > upper_level.
#define MASK_Z_LEVEL          (MASK_Z_LEVEL_1 | MASK_Z_LEVEL_2)
#define MASK_SADDLE_Z_LEVEL_1 0x0004 // saddle z > lower_level
#define MASK_SADDLE_Z_LEVEL_2 0x0008 // saddle z > upper_level
#define MASK_SADDLE           (MASK_SADDLE_Z_LEVEL_1 | MASK_SADDLE_Z_LEVEL_2)
#define MASK_BOUNDARY_N       0x0010 // N edge of quad is a boundary.
#define MASK_BOUNDARY_E       0x0020 // E edge of quad is a boundary.
#define MASK_EXISTS_QUAD      0x0040 // All of quad exists (is not masked).
#define MASK_EXISTS           MASK_EXISTS_QUAD
#define MASK_START_N          0x0080 // N to E
#define MASK_START_E          0x0100 // E to N
#define MASK_START_BOUNDARY_E 0x0200 // Filled and lines.
#define MASK_START_BOUNDARY_N 0x0400 // Filled and lines.
#define MASK_START_BOUNDARY_S 0x0800 // Filled only.
#define MASK_START_BOUNDARY_W 0x1000 // Filled only.
#define MASK_START_HOLE_N     0x2000 // N boundary of EXISTS, E to W, filled only.
#define MASK_ANY_START_FILLED (MASK_START_N | MASK_START_E | MASK_START_BOUNDARY_W | MASK_START_BOUNDARY_S | MASK_START_HOLE_N)
#define MASK_ANY_START_LINES  (MASK_START_N | MASK_START_E | MASK_START_BOUNDARY_W | MASK_START_BOUNDARY_S | MASK_START_BOUNDARY_N | MASK_START_BOUNDARY_E)
#define MASK_LOOK_N           0x4000
#define MASK_LOOK_S           0x8000
#define MASK_NO_STARTS_IN_ROW 0x10000
#define MASK_NO_MORE_STARTS   0x20000

// Accessors for various CacheItem masks.
#define Z_LEVEL(quad)          (_cache[quad] & MASK_Z_LEVEL)
#define Z_NE                   Z_LEVEL(POINT_NE)
#define Z_NW                   Z_LEVEL(POINT_NW)
#define Z_SE                   Z_LEVEL(POINT_SE)
#define Z_SW                   Z_LEVEL(POINT_SW)
#define SADDLE_SET(quad)       ((_cache[quad] & MASK_SADDLE) != MASK_SADDLE)
#define SADDLE_Z_LEVEL(quad)   (SADDLE_SET(quad) ? ((_cache[quad] & MASK_SADDLE) >> 2) : calc_z_level_mid(quad))
#define BOUNDARY_N(quad)       (_cache[quad] & MASK_BOUNDARY_N)
#define BOUNDARY_E(quad)       (_cache[quad] & MASK_BOUNDARY_E)
#define BOUNDARY_S(quad)       (_cache[quad-_nx] & MASK_BOUNDARY_N)
#define BOUNDARY_W(quad)       (_cache[quad-1] & MASK_BOUNDARY_E)
#define EXISTS_QUAD(quad)      ((_cache[quad] & MASK_EXISTS) == MASK_EXISTS_QUAD)
#define START_N(quad)          (_cache[quad] & MASK_START_N)
#define START_E(quad)          (_cache[quad] & MASK_START_E)
#define START_BOUNDARY_E(quad) (_cache[quad] & MASK_START_BOUNDARY_E)
#define START_BOUNDARY_N(quad) (_cache[quad] & MASK_START_BOUNDARY_N)
#define START_BOUNDARY_S(quad) (_cache[quad] & MASK_START_BOUNDARY_S)
#define START_BOUNDARY_W(quad) (_cache[quad] & MASK_START_BOUNDARY_W)
#define START_HOLE_N(quad)     (_cache[quad] & MASK_START_HOLE_N)
#define ANY_START_FILLED(quad) (_cache[quad] & MASK_ANY_START_FILLED)
#define ANY_START_LINES(quad)  (_cache[quad] & MASK_ANY_START_LINES)
#define LOOK_N(quad)           (_cache[quad] & MASK_LOOK_N)
#define LOOK_S(quad)           (_cache[quad] & MASK_LOOK_S)
#define NO_STARTS_IN_ROW(quad) (_cache[quad] & MASK_NO_STARTS_IN_ROW)
#define NO_MORE_STARTS(quad)   (_cache[quad] & MASK_NO_MORE_STARTS)


SerialContourGenerator::SerialContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y,
    const CoordinateArray& z, const MaskArray& mask, LineType line_type,
    FillType fill_type, long x_chunk_size, long y_chunk_size)
    : _x(x),
      _y(y),
      _z(z),
      _nx(_z.ndim() > 1 ? _z.shape(1) : 0),
      _ny(_z.ndim() > 0 ? _z.shape(0) : 0),
      _n(_nx*_ny),
      _nx_chunks(x_chunk_size == 0 ? 1
                                   : std::ceil((_nx-1.0) / x_chunk_size)),
      _ny_chunks(y_chunk_size == 0 ? 1
                                   : std::ceil((_ny-1.0) / y_chunk_size)),
      _n_chunks(_nx_chunks*_ny_chunks),
      _x_chunk_size(std::ceil((_nx-1.0) / _nx_chunks)),
      _y_chunk_size(std::ceil((_ny-1.0) / _ny_chunks)),
      _line_type(line_type),
      _fill_type(fill_type),
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
            throw std::invalid_argument("If mask is set it must be a 2D array with the same shape as z");
    }

    if (!supports_fill_type(fill_type))
        throw std::invalid_argument("Invalid FillType");

    if (x_chunk_size < 0 || y_chunk_size < 0)  // Check inputs, not calculated.
        throw std::invalid_argument("chunk_sizes cannot be negative");

    init_cache_grid(mask);
}

SerialContourGenerator::~SerialContourGenerator()
{
    delete _cache;
}

SerialContourGenerator::ZLevel SerialContourGenerator::calc_z_level_mid(
    long quad)
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

void SerialContourGenerator::closed_line(
    const Location& start_location, OuterOrHole outer_or_hole,
    ChunkLocal& local)
{
    assert(is_quad_in_chunk(start_location.quad, local));

    Location location = start_location;
    bool finished = false;
    unsigned long point_count = 0;

    if (outer_or_hole == Hole && local.pass == 0 && _identify_holes)
        set_look_flags(start_location.quad);

    while (!finished) {
        if (location.on_boundary)
            finished = follow_boundary(
                location, start_location, local, point_count);
        else
            finished = follow_interior(
                location, start_location, local, point_count);
        location.on_boundary = !location.on_boundary;
    }

    if (local.pass > 0) {
        local.line_offsets[local.line_count] = local.total_point_count;
        if (outer_or_hole == Outer && _identify_holes) {
            unsigned long outer_count = local.line_count - local.hole_count;
            local.outer_offsets[outer_count] = local.line_count;
        }
    }

    local.total_point_count += point_count;
    local.line_count++;
    if (outer_or_hole == Hole)
        local.hole_count++;
}

void SerialContourGenerator::closed_line_wrapper(
    const Location& start_location, OuterOrHole outer_or_hole,
    ChunkLocal& local)
{
    assert(is_quad_in_chunk(start_location.quad, local));

    if (local.pass == 0 || !_identify_holes) {
        closed_line(start_location, outer_or_hole, local);
    }
    else {
        assert(outer_or_hole == Outer);
        local.look_up_quads.clear();

        closed_line(start_location, outer_or_hole, local);

        for (unsigned int i = 0; i < local.look_up_quads.size(); ++i) {
            // Note that the collection can increase in size during this loop.
            long quad = local.look_up_quads[i];

            // Walk N to corresponding look S flag is reached.
            quad = find_look_S(quad);

            // Only 2 possible types of hole start:  start_E or start_hole_N.
            if (START_E(quad)) {
                Location location(quad, -1, Z_NE > 0, false);
                closed_line(location, Hole, local);
            }
            else { // _cache.start_hole_N(quad)
                Location location(quad, -1, false, true);
                closed_line(location, Hole, local);
            }
        }
    }
}

py::tuple SerialContourGenerator::contour_filled(
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

    init_cache_levels_and_starts();

    std::vector<py::list> return_lists(_return_list_count);

    ChunkLocal local;
    for (long chunk = 0; chunk < _n_chunks; ++chunk) {
        get_chunk_limits(chunk, local);
        single_chunk_filled(local, return_lists);
        local.clear();
    }

    py::tuple tuple(_return_list_count);
    for (unsigned int i = 0; i < _return_list_count; ++i)
        tuple[i] = return_lists[i];
    return tuple;
}

py::tuple SerialContourGenerator::contour_lines(const double& level)
{
    _filled = false;
    _lower_level = _upper_level = level;
    _identify_holes = false;
    _return_list_count = (_line_type == LineType::Separate) ? 1 : 2;

    init_cache_levels_and_starts();

    std::vector<py::list> return_lists(_return_list_count);

    ChunkLocal local;
    for (long chunk = 0; chunk < _n_chunks; ++chunk) {
        get_chunk_limits(chunk, local);
        single_chunk_lines(local, return_lists);
        local.clear();
    }

    py::tuple tuple(_return_list_count);
    for (unsigned int i = 0; i < _return_list_count; ++i)
        tuple[i] = return_lists[i];
    return tuple;
}

FillType SerialContourGenerator::default_fill_type()
{
    FillType fill_type = FillType::OuterCodes;
    assert(supports_fill_type(fill_type));
    return fill_type;
}

LineType SerialContourGenerator::default_line_type()
{
    LineType line_type = LineType::Separate;
    assert(supports_line_type(line_type));
    return line_type;
}

void SerialContourGenerator::export_filled(
    ChunkLocal& local, const std::vector<double>& all_points,
    std::vector<py::list>& return_lists)
{
    // all_points is only used for fill_types OuterCodes and OuterOffsets.

    switch (_fill_type)
    {
        case FillType::OuterCodes:
        case FillType::OuterOffsets: {
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
                        outer_end - outer_start + 1,
                        local.line_offsets.data() + outer_start, point_start));
            }
            break;
        }
        case FillType::ChunkCombinedCodes:
        case FillType::ChunkCombinedCodesOffsets:
            // return_lists[0] already set.
            assert(!local.line_offsets.empty());
            return_lists[1].append(Converter::convert_codes(
                local.total_point_count, local.line_offsets.size(),
                local.line_offsets.data()));

            if (_fill_type == FillType::ChunkCombinedCodesOffsets)
                return_lists[2].append(Converter::convert_offsets_nested(
                    local.outer_offsets.size(), local.outer_offsets.data(),
                    local.line_offsets.data()));
            break;
        case FillType::ChunkCombinedOffsets:
        case FillType::ChunkCombinedOffsets2:
            // return_lists[0] already set.
            assert(!local.line_offsets.empty());
            return_lists[1].append(Converter::convert_offsets(
                local.line_offsets.size(), local.line_offsets.data()));

            if (_fill_type == FillType::ChunkCombinedOffsets2)
                return_lists[2].append(Converter::convert_offsets(
                    local.outer_offsets.size(), local.outer_offsets.data()));
            break;
    }
}

void SerialContourGenerator::export_lines(
    ChunkLocal& local, const double* all_points_ptr,
    std::vector<py::list>& return_lists)
{
    switch (_line_type)
    {
        case LineType::Separate:
        case LineType::SeparateCodes:
            assert(all_points_ptr != nullptr);
            for (unsigned long i = 0; i < local.line_count; ++i) {
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
            break;
        case LineType::ChunkCombinedCodes: {
            // return_lists[0] already set.
            assert(all_points_ptr != nullptr);
            assert(!local.line_offsets.empty());
            return_lists[1].append(Converter::convert_codes_check_closed(
                local.total_point_count, local.line_offsets.size(),
                local.line_offsets.data(), all_points_ptr));
            break;
        }
        case LineType::ChunkCombinedOffsets:
            // return_lists[0] already set.
            assert(!local.line_offsets.empty());
            return_lists[1].append(Converter::convert_offsets(
                local.line_offsets.size(), local.line_offsets.data()));
            break;
    }
}

long SerialContourGenerator::find_look_S(long look_N_quad) const
{
    assert(_identify_holes);

    // Might need to be careful when looking in the same quad as the LOOK_UP.
    long quad = look_N_quad;

    // look_S quad must have 1 of only 2 possible types of hole start (start_E,
    // start_hole_N) but it may have other starts as well.

    // Start quad may be both a look_N and look_S quad.  Only want to stop
    // search here if look_S hole start is N of look_N.

    if (!LOOK_S(quad)) {
        do
        {
            quad += _nx;
            assert(quad >= 0 && quad < _n);
            assert(EXISTS_QUAD(quad));
        } while (!LOOK_S(quad));
    }

    return quad;
}

bool SerialContourGenerator::follow_boundary(
    Location& location, const Location& start_location, ChunkLocal& local,
    unsigned long& point_count)
{
    // forward values for boundaries:
    //     -1 = N boundary, E to W
    //     +1 = S boundary, W to E
    //   -_nx = W boundary, N to S
    //   +_nx = E boundary, S to N

    assert(is_quad_in_chunk(start_location.quad, local));
    assert(is_quad_in_chunk(location.quad, local));

    // Local variables for faster access.
    auto quad = location.quad;
    auto forward = location.forward;
    auto start_quad = start_location.quad;
    auto start_forward = start_location.forward;
    auto pass = local.pass;

    long start_point = (forward > 0 ? (forward == 1 ?  quad-_nx-1 : quad-_nx)
                                    : (forward == -1 ?  quad : quad-1));
    long end_point = start_point + forward;
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

        if (quad == start_quad && forward == start_forward) {
            if (start_location.on_boundary && point_count > 1) {
                // Polygon closed.
                finished = true;
                break;
            }
        }
        else if (pass == 0) {
            // Clear unwanted start locations.
            if (forward == +1 && START_BOUNDARY_S(quad))
                _cache[quad] &= ~MASK_START_BOUNDARY_S;
            else if (forward == -_nx && START_BOUNDARY_W(quad))
                _cache[quad] &= ~MASK_START_BOUNDARY_W;
            else if (forward == -1 && START_HOLE_N(quad))
                _cache[quad] &= ~MASK_START_HOLE_N;
        }

        // Check if need to leave boundary into interior.
        if (end_z != 1) {
            location.is_upper = (end_z == 2);  // Leave via this level.
            forward = (forward > 0 ? (forward == 1 ? _nx : -1)  // i.e. left
                                   : (forward == -1 ? -_nx : 1));
            break;
        }

        // Add end point.
        point_count++;
        if (pass > 0) {
            get_point_xy(end_point, local.points);

            if (forward == 1 && LOOK_N(quad) && _identify_holes) {
                assert(BOUNDARY_N(quad-_nx));
                local.look_up_quads.push_back(quad);
            }
        }

        move_to_next_boundary_edge(quad, forward);

        start_point = end_point;
        start_z = end_z;
        end_point = start_point + forward;
        end_z = Z_LEVEL(end_point);
    }

    location.quad = quad;
    location.forward = forward;

    return finished;
}

bool SerialContourGenerator::follow_interior(
    Location& location, const Location& start_location, ChunkLocal& local,
    unsigned long& point_count)
{
    // Adds the start point in each quad visited, but not the end point unless
    // closing the polygon.
    // Only need to consider a single level of course.
    assert(is_quad_in_chunk(start_location.quad, local));
    assert(is_quad_in_chunk(location.quad, local));

    // Local variables for faster access.
    auto quad = location.quad;
    auto forward = location.forward;
    auto is_upper = location.is_upper;
    auto start_quad = start_location.quad;
    auto start_forward = start_location.forward;
    auto pass = local.pass;

    // Indices of points on entry edge.
    long left = (forward > 0 ? (forward == 1 ? _nx : -1)
                             : (forward == -1 ? -_nx : 1));
    long left_point = (forward > 0 ? (forward == 1 ? quad-1 : quad-_nx-1)
                                   : (forward == -1 ? quad-_nx : quad));
    long right_point = left_point - left;

    bool want_look_N = _identify_holes && pass > 0;

    bool abort = false;     // Whether to about the loop.
    bool finished = false;  // Whether finished line, i.e. returned to start.
    while (!abort) {
        assert(is_quad_in_chunk(quad, local));
        assert(is_point_in_chunk(left_point, local));
        assert(is_point_in_chunk(right_point, local));

        if (pass > 0)
            interp(left_point, right_point, is_upper, local);
        point_count++;

        if (quad == start_quad && forward == start_forward &&
            is_upper == start_location.is_upper &&
            !start_location.on_boundary && point_count > 1) {
            finished = true;  // Polygon closed, exit immediately.
            break;
        }

        // Indices and z_levels of the opposite points.
        long opposite_left_point = left_point + forward;
        long opposite_right_point = right_point + forward;
        ZLevel z_opposite_left = Z_LEVEL(opposite_left_point);
        ZLevel z_opposite_right = Z_LEVEL(opposite_right_point);

        // Turn left (1), move forward (0) or turn right (-1).
        int turn_left = -1;
        ZLevel z_test = is_upper ? 2 : 0;
        if (z_opposite_left == z_test) {
            if (z_opposite_right == z_test || SADDLE_Z_LEVEL(quad) == z_test)
                turn_left = 1;
        }
        else if (z_opposite_right == z_test)
            turn_left = 0;

        // Clear unwanted start locations.
        if (pass == 0 && !(quad == start_quad && forward == start_forward)) {
            if (START_E(quad) && forward == -1 && turn_left == -1 &&
                (is_upper ? Z_NE > 0 : Z_NE < 2)) {
                _cache[quad] &= ~MASK_START_E;  // E high if is_upper else low.

                if (!_filled && quad < start_location.quad)
                    // Already counted points from here onwards.
                    break;
            }
            else if (START_N(quad) && forward < -1 && turn_left == 1 &&
                     (is_upper ? Z_NW > 0 : Z_NW < 2)) {
                _cache[quad] &= ~MASK_START_N;  // E high if is_upper else low.

                if (!_filled && quad < start_location.quad)
                    // Already counted points from here onwards.
                    break;
            }
        }

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
        else {  // Straight on.
            left_point = opposite_left_point;
            right_point = opposite_right_point;
            // Edge stays the same.
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

        // If reached a boundary, return.
        // quad is always unchanged here.
        bool reached_boundary = false;
        if (forward == 1 && BOUNDARY_E(quad)) {
            forward = _nx;  // Moving N.
            reached_boundary = true;
        }
        else if (forward > 1 && BOUNDARY_N(quad)) {
            forward = -1;  // Moving W.
            reached_boundary = true;
        }
        else if (forward == -1 && BOUNDARY_W(quad)) {
            forward = -_nx;  // Moving S.
            reached_boundary = true;
        }
        else if (forward < -1 && BOUNDARY_S(quad)) {
            forward = 1;  // Moving E.
            reached_boundary = true;
        }

        if (reached_boundary) {
            if (!_filled) {
                point_count++;
                if (pass > 0)
                    interp(left_point, right_point, false, local);
            }
            break;
        }

        quad += forward;
    }

    location.quad = quad;
    location.forward = forward;
    location.is_upper = is_upper;

    return finished;
}

py::tuple SerialContourGenerator::get_chunk_count() const
{
    py::tuple tuple(2);
    tuple[0] = _ny_chunks;
    tuple[1] = _nx_chunks;
    return tuple;
}

void SerialContourGenerator::get_chunk_limits(
    long chunk, ChunkLocal& local) const
{
    assert(chunk >= 0 && chunk < _n_chunks && "chunk index out of bounds");

    local.chunk = chunk;

    long ichunk = chunk % _nx_chunks;
    long jchunk = chunk / _nx_chunks;

    local.istart = ichunk*_x_chunk_size + 1;
    local.iend = (ichunk < _nx_chunks-1 ? (ichunk+1)*_x_chunk_size : _nx-1);

    local.jstart = jchunk*_y_chunk_size + 1;
    local.jend = (jchunk < _ny_chunks-1 ? (jchunk+1)*_y_chunk_size : _ny-1);
}

py::tuple SerialContourGenerator::get_chunk_size() const
{
    py::tuple tuple(2);
    tuple[0] = _y_chunk_size;
    tuple[1] = _x_chunk_size;
    return tuple;
}

bool SerialContourGenerator::get_corner_mask() const
{
    return false;
}

FillType SerialContourGenerator::get_fill_type() const
{
    return _fill_type;
}

LineType SerialContourGenerator::get_line_type() const
{
    return _line_type;
}

void SerialContourGenerator::get_point_xy(long point, double*& points) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    *points++ = _x.data()[point];
    *points++ = _y.data()[point];
}

const double& SerialContourGenerator::get_point_x(long point) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    return _x.data()[point];
}

const double& SerialContourGenerator::get_point_y(long point) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    return _y.data()[point];
}

const double& SerialContourGenerator::get_point_z(long point) const
{
    assert(point >= 0 && point < _n && "point index out of bounds");
    return _z.data()[point];
}

void SerialContourGenerator::init_cache_grid(const MaskArray& mask)
{
    long i, j, quad;
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

                if (i > 0 && j > 0 &&
                    !(mask_ptr[POINT_NW] || mask_ptr[POINT_NE] ||
                      mask_ptr[POINT_SW] || mask_ptr[POINT_SE]))
                    _cache[quad] |= MASK_EXISTS_QUAD;
            }
        }

        // Stage 2, calculate N and E boundaries.  For each quad use boundary
        // data already calculated for quads to W and S, so must iterate
        // through quads in correct order (increasing i and j indices).
        // Cannot use boundary data for quads to E and N as have not yet
        // calculated it.
        quad = 0;
        for (j = 0; j < _ny; ++j) {
            for (i = 0; i < _nx; ++i, ++quad) {
                bool E_exists_quad = (i < _nx-1 && EXISTS_QUAD(quad+1));
                bool N_exists_quad = (j < _ny-1 && EXISTS_QUAD(quad+_nx));
                bool exists = EXISTS_QUAD(quad);

                if (exists != E_exists_quad ||
                    (i % _x_chunk_size == 0 && exists && E_exists_quad))
                    _cache[quad] |= MASK_BOUNDARY_E;

                if (exists != N_exists_quad ||
                    (j % _y_chunk_size == 0 && exists && N_exists_quad))
                    _cache[quad] |= MASK_BOUNDARY_N;
            }
        }
    }
}

void SerialContourGenerator::init_cache_levels_and_starts()
{
    const double* z_ptr = _z.data();
    CacheItem keep_mask = MASK_EXISTS_QUAD | MASK_BOUNDARY_N | MASK_BOUNDARY_E;

    if (_filled) {
        long quad = 0;
        long j_final_start = 0;
        for (long j = 0; j < _ny; ++j) {
            ZLevel z_nw = 0, z_sw = 0;
            bool start_in_row = false;
            for (long i = 0; i < _nx; ++i, ++quad, ++z_ptr) {
                _cache[quad] &= keep_mask;
                _cache[quad] |= MASK_SADDLE;

                // Cache z-level of NE point.
                ZLevel z_ne = 0;
                if (*z_ptr > _upper_level) {
                    _cache[quad] |= MASK_Z_LEVEL_2;
                    z_ne = 2;
                }
                else if (*z_ptr > _lower_level) {
                    _cache[quad] |= MASK_Z_LEVEL_1;
                    z_ne = 1;
                }

                // z-level of SE point already calculated if j > 0; not needed
                // if j == 0.
                ZLevel z_se = (j > 0 ? Z_SE : 0);

                if (EXISTS_QUAD(quad)) {
                    if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                        (z_sw == 0 || SADDLE_Z_LEVEL(quad) == 0)) {
                        _cache[quad] |= MASK_START_N;  // N to E low.
                        start_in_row = true;
                    }
                    else if (z_nw == 2 && z_se == 2 && z_ne < 2 &&
                             (z_sw == 2 || SADDLE_Z_LEVEL(quad) == 2)) {
                        _cache[quad] |= MASK_START_N;  // N to E high.
                        start_in_row = true;
                    }

                    if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                        (z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                        _cache[quad] |= MASK_START_E;  // E to N low.
                        start_in_row = true;
                    }
                    else if (z_ne == 2 && z_nw < 2 && z_se < 2 &&
                             (z_sw < 2 || SADDLE_Z_LEVEL(quad) < 2)) {
                        _cache[quad] |= MASK_START_E;  // E to N high.
                        start_in_row = true;
                    }

                    if (BOUNDARY_S(quad) &&
                        ((z_sw == 2 && z_se < 2) || (z_sw == 0 && z_se > 0) ||
                         z_sw == 1)) {
                        _cache[quad] |= MASK_START_BOUNDARY_S;
                        start_in_row = true;
                    }

                    if (BOUNDARY_W(quad) &&
                        ((z_nw == 2 && z_sw < 2) || (z_nw == 0 && z_sw > 0) ||
                         (z_nw == 1 && z_sw != 1))) {
                        _cache[quad] |= MASK_START_BOUNDARY_W;
                        start_in_row = true;
                    }

                    // Start following N boundary from E to W which is a hole.
                    // Required for an internal masked region which is a hole in
                    // a filled polygon.
                    if (BOUNDARY_N(quad) && z_nw == 1 && z_ne == 1 &&
                        !START_HOLE_N(quad-1) &&
                        j % _y_chunk_size != 0 &&
                        //j % _y_chunk_size != _y_chunk_size-1 &&
                        j != _ny-1) {
                        _cache[quad] |= MASK_START_HOLE_N;
                        start_in_row = true;
                    }
                }

                z_nw = z_ne;
                z_sw = z_se;
            } // i-loop.

            if (start_in_row)
                j_final_start = j;
            else
                _cache[1 + j*_nx] |= MASK_NO_STARTS_IN_ROW;
        } // j-loop.

        if (j_final_start < _ny-1)
            _cache[1 + (j_final_start+1)*_nx] |= MASK_NO_MORE_STARTS;
    }
    else {
        long quad = 0;
        long j_final_start = 0;
        for (long j = 0; j < _ny; ++j) {
            ZLevel z_nw = 0, z_sw = 0;
            bool start_in_row = false;
            for (long i = 0; i < _nx; ++i, ++quad, ++z_ptr) {
                _cache[quad] &= keep_mask;
                _cache[quad] |= MASK_SADDLE;

                // Cache z-level of NE point.
                ZLevel z_ne = 0;
                if (*z_ptr > _lower_level) {
                    _cache[quad] |= MASK_Z_LEVEL_1;
                    z_ne = 1;
                }

                // z-level of SE point already calculated if j > 0; not needed
                // if j == 0.
                ZLevel z_se = (j > 0 ? Z_SE : 0);

                if (EXISTS_QUAD(quad)) {
                    if (BOUNDARY_S(quad) && z_sw == 1 && z_se == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_S;
                        start_in_row = true;
                    }

                    if (BOUNDARY_W(quad) && z_nw == 1 && z_sw == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_W;
                        start_in_row = true;
                    }

                    if (BOUNDARY_E(quad) && z_se == 1 && z_ne == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_E;
                        start_in_row = true;
                    }

                    if (BOUNDARY_N(quad) && z_ne == 1 && z_nw == 0) {
                        _cache[quad] |= MASK_START_BOUNDARY_N;
                        start_in_row = true;
                    }

                    if (!BOUNDARY_N(quad) && !BOUNDARY_E(quad)) {
                        if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                            (z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                            _cache[quad] |= MASK_START_E;  // E to N low.
                            start_in_row = true;
                        }
                        else if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                                 (z_sw == 0 || SADDLE_Z_LEVEL(quad) == 0)) {
                            _cache[quad] |= MASK_START_N;  // N to E low.
                            start_in_row = true;
                        }
                    }
                }

                z_nw = z_ne;
                z_sw = z_se;
            } // i-loop.

            if (start_in_row)
                j_final_start = j;
            else
                _cache[1 + j*_nx] |= MASK_NO_STARTS_IN_ROW;
        } // j-loop.

        if (j_final_start < _ny-1)
            _cache[1 + (j_final_start+1)*_nx] |= MASK_NO_MORE_STARTS;
    }
}

void SerialContourGenerator::interp(
    long point0, long point1, bool is_upper, ChunkLocal& local) const
{
    // point0 and 1 are point numbers.
    assert(is_point_in_chunk(point0, local));
    assert(is_point_in_chunk(point1, local));

    const double& z1 = get_point_z(point1);
    const double& level = is_upper ? _upper_level : _lower_level;
    double frac = (z1 - level) / (z1 - get_point_z(point0));
    assert(frac >= 0.0 && frac <= 1.0 && "Interp fraction out of bounds");

    *local.points++ =
        get_point_x(point0)*frac + get_point_x(point1)*(1.0 - frac);
    *local.points++ =
        get_point_y(point0)*frac + get_point_y(point1)*(1.0 - frac);
}

bool SerialContourGenerator::is_point_in_chunk(
    long point, const ChunkLocal& local) const
{
    return is_quad_in_bounds(
        point, local.istart-1, local.iend, local.jstart-1, local.jend);
}

bool SerialContourGenerator::is_quad_in_bounds(
    long quad, long istart, long iend, long jstart, long jend) const
{
    return (quad % _nx >= istart && quad % _nx <= iend &&
            quad / _nx >= jstart && quad / _nx <= jend);
}

bool SerialContourGenerator::is_quad_in_chunk(
    long quad, const ChunkLocal& local) const
{
    return is_quad_in_bounds(
        quad, local.istart, local.iend, local.jstart, local.jend);
}

void SerialContourGenerator::line(
    const Location& start_location, ChunkLocal& local)
{
    // start_location.on_boundary indicates starts (and therefore also finishes)

    assert(is_quad_in_chunk(start_location.quad, local));

    Location location = start_location;
    unsigned long point_count = 0;

    // finished == true indicates closed line loop.
    bool finished = follow_interior(
        location, start_location, local, point_count);

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

void SerialContourGenerator::move_to_next_boundary_edge(
    long& quad, long& forward) const
{
    // edge == 0 for E edge (facing N), forward = +_nx
    //         1 for S edge (facing E), forward = +1
    //         2 for W edge (facing S), forward = -_nx
    //         3 for N edge (facing W), forward = -1
    int edge = 0;

    // Need index of quad that is the same as the end point, i.e. quad to SW of
    // end point.  Looking for next boundary edge of this end point given the
    // start forward direction.
    if (forward == -1) {
        quad -= 1;  // N edge facing W.
        edge = 3;
    }
    else if (forward == -_nx) {
        quad -= _nx+1;  // W edge facing S.
        edge = 2;
    }
    else if (forward == 1) {
        quad -= _nx;  // S edge facing E.
        edge = 1;
    }
    // else W edge facing N, no change to quad.

    while (true) {
        // Look at possible edges that leave NE point of quad.
        // If something is wrong here or in the setup of the boundary flags,
        // can end up with an infinite loop!
        switch (edge) {
            case 0:
                // Is there an edge to follow to W?
                if (BOUNDARY_N(quad)) {
                    forward = -1;
                    return;
                }
                break;
            case 1:
                // Is there an edge to follow to N?
                if (BOUNDARY_E(quad+_nx)) {  // Really a BOUNDARY_W check.
                    forward = _nx;
                    quad += _nx;
                    return;
                }
                break;
            case 2:
                // Is there an edge to follow to E?
                if (BOUNDARY_N(quad+1)) {  // Really a BOUNDARY_S check
                    forward = 1;
                    quad += _nx+1;
                    return;
                }
                break;
            case 3:
                // Is there an edge to follow to S?
                if (BOUNDARY_E(quad)) {
                    forward = -_nx;
                    quad += 1;
                    return;
                }
                break;
            default:
                assert(0 && "Invalid edge index");
                break;
        }

        edge = (edge + 1) % 4;
    }
}

void SerialContourGenerator::set_look_flags(long hole_start_quad)
{
    assert(_identify_holes);

    // The only possible hole starts are start_E (from E to N) and start_hole_N
    // (on N boundary, E to W).
    assert(hole_start_quad >= 0 && hole_start_quad < _n);
    assert(EXISTS_QUAD(hole_start_quad));
    assert(!LOOK_S(hole_start_quad) && "Look S already set");

    _cache[hole_start_quad] |= MASK_LOOK_S;

    // Walk S until find place to mark corresponding look N.
    long quad = hole_start_quad;

    while (true) {
        assert(quad >= 0 && quad < _n);
        assert(EXISTS_QUAD(quad));

        if (!EXISTS_QUAD(quad-_nx) || Z_SE != 1) {
            assert(!LOOK_N(quad) && "Look N already set");
            _cache[quad] |= MASK_LOOK_N;
            break;
        }

        quad -= _nx;
    }
}

void SerialContourGenerator::single_chunk_filled(
    ChunkLocal& local, std::vector<py::list>& return_lists)
{
    // Allocated at end of pass 0, depending on _fill_type.
    std::vector<double> all_points;

    for (local.pass = 0; local.pass < 2; ++local.pass) {
        bool ignore_holes = (_identify_holes && local.pass == 1);

        long j_final_start = local.jstart;
        for (long j = local.jstart; j <= local.jend; ++j) {
            long quad = local.istart + j*_nx;

            if (NO_MORE_STARTS(quad))
                break;

            if (NO_STARTS_IN_ROW(quad))
                continue;

            // Want to count number of starts in this row, so store how many
            // starts at start of row.
            unsigned long prev_start_count =
                (_identify_holes ? local.line_count - local.hole_count
                                 : local.line_count);

            for (long i = local.istart; i <= local.iend; ++i, ++quad) {
                if (!ANY_START_FILLED(quad))
                    continue;

                if (EXISTS_QUAD(quad)) {
                    if (START_BOUNDARY_S(quad)) {
                        Location location(quad, 1, Z_SW == 2, true);
                        closed_line_wrapper(location, Outer, local);
                    }

                    if (START_BOUNDARY_W(quad)) {
                        Location location(quad, -_nx, Z_NW == 2, true);
                        closed_line_wrapper(location, Outer, local);
                    }

                    if (START_N(quad)) {
                        Location location(quad, -_nx, Z_NW > 0, false);
                        closed_line_wrapper(location, Outer, local);
                    }

                    if (ignore_holes)
                        continue;

                    if (START_E(quad)) {
                        Location location(quad, -1, Z_NE > 0, false);
                        closed_line_wrapper(location, Hole, local);
                    }

                    if (START_HOLE_N(quad)) {
                        Location location(quad, -1, false, true);
                        closed_line_wrapper(location, Hole, local);
                    }
                }
            } // i

            // Number of starts at end of row.
            unsigned long start_count =
                (_identify_holes ? local.line_count - local.hole_count
                                 : local.line_count);
            if (start_count - prev_start_count)
                j_final_start = j;
            else
                _cache[local.istart + j*_nx] |= MASK_NO_STARTS_IN_ROW;
        } // j

        if (j_final_start < local.jend)
            _cache[local.istart + (j_final_start+1)*_nx] |= MASK_NO_MORE_STARTS;

        if (local.pass == 0) {
            if (_fill_type == FillType::OuterCodes ||
                _fill_type == FillType::OuterOffsets) {
                all_points.resize(2*local.total_point_count);

                // Where to store contour points.
                local.points = all_points.data();
            }
            else {  // Combined points.
                py::size_t points_shape[2] = {local.total_point_count, 2};
                PointArray py_all_points(points_shape);
                return_lists[0].append(py_all_points);

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

    if (0) {
        std::cout << "total_point_count: " << local.total_point_count << std::endl;
        std::cout << "line_count: " << local.line_count << std::endl;
        std::cout << "hole_count: " << local.hole_count << std::endl;

        std::cout << "line_offsets (" << local.line_offsets.size() << ")";
        for (const auto& i : local.line_offsets)
            std::cout << " " << i;
        std::cout << std::endl;

        std::cout << "outer_offsets (" << local.outer_offsets.size() << ")";
        for (const auto& i : local.outer_offsets)
            std::cout << " " << i;
        std::cout << std::endl;
    }

    // Check both passes returned same number of points, lines, etc.
    assert(local.line_offsets.size() == local.line_count + 1);
    assert(local.line_offsets.back() == local.total_point_count);

    if (_identify_holes) {
        assert(local.outer_offsets.size() ==
               local.line_count - local.hole_count + 1);
        assert(local.outer_offsets.back() == local.line_count);
    }
    else {
        assert(local.outer_offsets.empty());
    }

    if (local.total_point_count > 0)
        export_filled(local, all_points, return_lists);
}

void SerialContourGenerator::single_chunk_lines(
    ChunkLocal& local, std::vector<py::list>& return_lists)
{
    // Allocated at end of pass 0, depending on _line_type.
    std::vector<double> all_points;
    const double* all_points_ptr = nullptr;

    for (local.pass = 0; local.pass < 2; ++local.pass) {
        long j_final_start = local.jstart;
        for (long j = local.jstart; j <= local.jend; ++j) {
            long quad = local.istart + j*_nx;

            if (NO_MORE_STARTS(quad))
                break;

            if (NO_STARTS_IN_ROW(quad))
                continue;

            // Want to count number of starts in this row, so store how many
            // starts at start of row.
            unsigned long prev_start_count = local.line_count;

            for (long i = local.istart; i <= local.iend; ++i, ++quad) {
                if (!ANY_START_LINES(quad))
                    continue;

                if (EXISTS_QUAD(quad)) {
                    if (START_BOUNDARY_S(quad)) {
                        Location location(quad, _nx, false, true);
                        line(location, local);
                    }

                    if (START_BOUNDARY_W(quad)) {
                        Location location(quad, 1, false, true);
                        line(location, local);
                    }

                    if (START_BOUNDARY_E(quad)) {
                        Location location(quad, -1, false, true);
                        line(location, local);
                    }

                    if (START_BOUNDARY_N(quad)) {
                        Location location(quad, -_nx, false, true);
                        line(location, local);
                    }

                    if (START_E(quad)) {
                        Location location(quad, -1, false, false);
                        line(location, local);
                    }

                    if (START_N(quad)) {
                        Location location(quad, -_nx, false, false);
                        line(location, local);
                    }
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
            if (_line_type == LineType::Separate ||
                _line_type == LineType::SeparateCodes) {
                all_points.resize(2*local.total_point_count);

                // Where to store contour points.
                local.points = all_points.data();

                // Needed to check if lines are closed loops or not.
                all_points_ptr = all_points.data();
            }
            else {  // Combined points.
                py::size_t points_shape[2] = {local.total_point_count, 2};
                PointArray py_all_points(points_shape);
                return_lists[0].append(py_all_points);

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

    if (local.total_point_count > 0)
        export_lines(local, all_points_ptr, return_lists);
}

bool SerialContourGenerator::supports_fill_type(FillType fill_type)
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

bool SerialContourGenerator::supports_line_type(LineType line_type)
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

void SerialContourGenerator::write_cache() const
{
    std::cout << "---------- Cache ----------" << std::endl;
    long ny = _n / _nx;
    for (long j = ny-1; j >= 0; --j) {
        std::cout << "j=" << j << " ";
        for (long i = 0; i < _nx; ++i) {
            long quad = i + j*_nx;
            write_cache_quad(quad);
        }
        std::cout << std::endl;
    }
    std::cout << "    ";
    for (long i = 0; i < _nx; ++i)
        std::cout << "i=" << i << "         ";
    std::cout << std::endl;
    std::cout << "---------------------------" << std::endl;
}

void SerialContourGenerator::write_cache_quad(long quad) const
{
    assert(quad >= 0 && quad < _n && "quad index out of bounds");
    std::cout << (NO_MORE_STARTS(quad) ? 'x' :
                    (NO_STARTS_IN_ROW(quad) ? 'i' : '.'));
    std::cout << (EXISTS_QUAD(quad) ? 'q' : '.');
    std::cout << (BOUNDARY_N(quad) && BOUNDARY_E(quad) ? 'b' : (
                    BOUNDARY_N(quad) ? 'n' : (BOUNDARY_E(quad) ? 'e' : '.')));
    std::cout << Z_LEVEL(quad);
    std::cout << ((_cache[quad] & MASK_SADDLE) >> 2);
    std::cout << (START_BOUNDARY_E(quad) ? 'e' : '.');
    std::cout << (START_BOUNDARY_N(quad) ? 'n' : '.');
    if (!_filled) {
        std::cout << (START_BOUNDARY_S(quad) ? 's' : '.');
        std::cout << (START_BOUNDARY_W(quad) ? 'w' : '.');
    }
    std::cout << (START_E(quad) ? 'E' : '.');
    std::cout << (START_N(quad) ? 'N' : '.');
    if (_filled) {
        std::cout << (START_HOLE_N(quad) ? 'h' : '.');
        std::cout << (LOOK_N(quad) && LOOK_S(quad) ? 'B' :
            (LOOK_N(quad) ? '^' : (LOOK_S(quad) ? 'v' : '.')));
    }
    std::cout << ' ';
}
