#ifndef CONTOURPY_SERIAL_H
#define CONTOURPY_SERIAL_H

#include "common.h"
#include "fill_type.h"
#include "line_type.h"
#include "outer_or_hole.h"
#include <vector>

// Forward declarations.
class ChunkLocal;

class SerialContourGenerator
{
public:
    SerialContourGenerator(
        const CoordinateArray& x, const CoordinateArray& y,
        const CoordinateArray& z, const MaskArray& mask, LineType line_type,
        FillType fill_type, long x_chunk_size, long y_chunk_size);

    ~SerialContourGenerator();

    py::tuple contour_filled(
        const double& lower_level, const double& upper_level);

    py::tuple contour_lines(const double& level);

    static FillType default_fill_type();
    static LineType default_line_type();

    py::tuple get_chunk_count() const;

    py::tuple get_chunk_size() const;

    bool get_corner_mask() const;

    FillType get_fill_type() const;
    LineType get_line_type() const;

    static bool supports_fill_type(FillType fill_type);
    static bool supports_line_type(LineType line_type);

    void write_cache() const;  // For debug purposes only.

private:
    typedef uint32_t CacheItem;
    typedef CacheItem ZLevel;

    struct Location
    {
        Location(long quad_, long forward_, bool is_upper_, bool on_boundary_)
            : quad(quad_), forward(forward_), is_upper(is_upper_),
              on_boundary(on_boundary_)
        {}

        long quad;
        long forward;
        bool is_upper;
        bool on_boundary;
    };

    ZLevel calc_z_level_mid(long quad);

    void closed_line(
        const Location& start_location, OuterOrHole outer_or_hole,
        ChunkLocal& local);

    void closed_line_wrapper(
        const Location& start_location, OuterOrHole outer_or_hole,
        ChunkLocal& local);

    long find_look_S(long look_N_quad) const;

    // Return true if finished (i.e. back to start quad, direction and upper).
    bool follow_boundary(
        Location& location, const Location& start_location, ChunkLocal& local,
        unsigned long& point_count);

    // Return true if finished (i.e. back to start quad, direction and upper).
    bool follow_interior(
        Location& location, const Location& start_location, ChunkLocal& local,
        unsigned long& point_count);

    // These are quad chunk limits, not point chunk limits.
    // chunk is index in range 0.._n_chunks-1.
    void get_chunk_limits(long chunk, ChunkLocal& local) const;

    void get_point_xy(long point, double*& points) const;

    const double& get_point_x(long point) const;
    const double& get_point_y(long point) const;
    const double& get_point_z(long point) const;

    void init_cache_grid(const MaskArray& mask);

    void init_cache_levels_and_starts();

    // Increments local.points twice.
    void interp(
        long point0, long point1, bool is_upper, ChunkLocal& local) const;

    bool is_point_in_chunk(long point, const ChunkLocal& local) const;

    bool is_quad_in_bounds(
        long quad, long istart, long iend, long jstart, long jend) const;

    bool is_quad_in_chunk(long quad, const ChunkLocal& local) const;

    void line(const Location& start_location, ChunkLocal& local);

    void move_to_next_boundary_edge(long& quad, long& forward) const;

    void set_look_flags(long hole_start_quad);

    void single_chunk_filled(
        long chunk, ChunkLocal& local, std::vector<py::list>& return_lists);

    void single_chunk_lines(
        long chunk, ChunkLocal& local, std::vector<py::list>& return_lists);

    void write_cache_quad(long quad) const;



    const CoordinateArray _x, _y, _z;
    const long _nx, _ny;                // Number of points in each direction.
    const long _n;                      // Total number of points (and quads).
    const long _nx_chunks, _ny_chunks;  // Number of chunks in each direction.
    const long _n_chunks;               // Total number of chunks.
    const long _x_chunk_size, _y_chunk_size;
    const LineType _line_type;
    const FillType _fill_type;

    CacheItem* _cache;

    // Current contouring operation.
    bool _filled;
    double _lower_level, _upper_level;

    // Current contouring operation, based on return type and filled or lines.
    bool _identify_holes;
    unsigned int _return_list_count;
};

#endif // CONTOURPY_SERIAL_H
