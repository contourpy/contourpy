// BaseContourGenerator class provides functionality common to multiple contouring algorithms.
// Uses the Curiously Recurring Template Pattern idiom whereby classes derived from this are
// declared as
//     class Derived : public BaseContourGenerator<Derived>
//
// It provides static polymorphism at compile-time rather than the more common dynamic polymorphism
// at run-time using virtual functions.  Hence it avoids the runtime overhead of calling virtual
// functions.

#ifndef CONTOURPY_BASE_H
#define CONTOURPY_BASE_H

#include "chunk_local.h"
#include "fill_type.h"
#include "interp.h"
#include "line_type.h"
#include "outer_or_hole.h"
#include <vector>

template <typename Derived>
class BaseContourGenerator
{
public:
    ~BaseContourGenerator();

    static FillType default_fill_type();
    static LineType default_line_type();

    py::tuple get_chunk_count() const;  // Return (y_chunk_count, x_chunk_count)
    py::tuple get_chunk_size() const;   // Return (y_chunk_size, x_chunk_size)

    bool get_corner_mask() const;

    FillType get_fill_type() const;
    LineType get_line_type() const;

    py::sequence filled(const double& lower_level, const double& upper_level);
    py::sequence lines(const double& level);

    static bool supports_fill_type(FillType fill_type);
    static bool supports_line_type(LineType line_type);

    void write_cache() const;  // For debug purposes only.

    // Non-copyable and non-moveable.
    BaseContourGenerator(const BaseContourGenerator& other) = delete;
    BaseContourGenerator(const BaseContourGenerator&& other) = delete;
    BaseContourGenerator& operator=(const BaseContourGenerator& other) = delete;
    BaseContourGenerator& operator=(const BaseContourGenerator&& other) = delete;

protected:
    BaseContourGenerator(
        const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
        const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type,
        Interp interp, index_t x_chunk_size, index_t y_chunk_size);

    typedef uint32_t CacheItem;
    typedef CacheItem ZLevel;

    struct Location
    {
        Location(index_t quad_, index_t forward_, index_t left_, bool is_upper_, bool on_boundary_)
            : quad(quad_), forward(forward_), left(left_), is_upper(is_upper_),
              on_boundary(on_boundary_)
        {}

        friend std::ostream &operator<<(std::ostream &os, const Location& location)
        {
            os << "quad=" << location.quad << " forward=" << location.forward << " left="
                << location.left << " is_upper=" << location.is_upper << " on_boundary="
                << location.on_boundary;
            return os;
        }

        index_t quad, forward, left;
        bool is_upper, on_boundary;
    };

    // Calculate and set z-level of saddle quad.
    ZLevel calc_z_level_mid(index_t quad);

    void closed_line(const Location& start_location, OuterOrHole outer_or_hole, ChunkLocal& local);

    void closed_line_wrapper(
        const Location& start_location, OuterOrHole outer_or_hole, ChunkLocal& local);

    // Write points and offsets/codes to output numpy arrays.
    void export_filled(
        ChunkLocal& local, const std::vector<double>& all_points,
        std::vector<py::list>& return_lists);

    void export_lines(
        ChunkLocal& local, const double* all_points_ptr, std::vector<py::list>& return_lists);

    index_t find_look_S(index_t look_N_quad) const;

    // Return true if finished (i.e. back to start quad, direction and upper).
    bool follow_boundary(
        Location& location, const Location& start_location, ChunkLocal& local, size_t& point_count);

    // Return true if finished (i.e. back to start quad, direction and upper).
    bool follow_interior(
        Location& location, const Location& start_location, ChunkLocal& local, size_t& point_count);

    index_t get_boundary_start_point(const Location& location) const;

    // These are quad chunk limits, not point chunk limits.
    // chunk is index in range 0.._n_chunks-1.
    void get_chunk_limits(index_t chunk, ChunkLocal& local) const;

    index_t get_interior_start_left_point(
        const Location& location, bool& start_corner_diagonal) const;

    index_t get_n_chunks() const;

    void get_point_xy(index_t point, double*& points) const;

    const double& get_point_x(index_t point) const;
    const double& get_point_y(index_t point) const;
    const double& get_point_z(index_t point) const;

    void init_cache_grid(const MaskArray& mask);

    // Either for a single chunk, or the whole domain (all chunks) if local == nullptr.
    void init_cache_levels_and_starts(const ChunkLocal* local = nullptr);

    // Increments local.points twice.
    void interp(index_t point0, index_t point1, bool is_upper, ChunkLocal& local) const;

    bool is_filled() const;

    bool is_point_in_chunk(index_t point, const ChunkLocal& local) const;

    bool is_quad_in_bounds(
        index_t quad, index_t istart, index_t iend, index_t jstart, index_t jend) const;

    bool is_quad_in_chunk(index_t quad, const ChunkLocal& local) const;

    void line(const Location& start_location, ChunkLocal& local);

    void march_chunk(ChunkLocal& local, std::vector<py::list>& return_lists);

    py::sequence march_wrapper();

    void move_to_next_boundary_edge(index_t& quad, index_t& forward, index_t& left) const;

    void set_look_flags(index_t hole_start_quad);

    void write_cache_quad(index_t quad) const;

    ZLevel z_to_zlevel(const double& z_value);


private:
    const CoordinateArray _x, _y, _z;
    const index_t _nx, _ny;                // Number of points in each direction.
    const index_t _n;                      // Total number of points (and quads).
    const index_t _x_chunk_size, _y_chunk_size;
    const index_t _nx_chunks, _ny_chunks;  // Number of chunks in each direction.
    const index_t _n_chunks;               // Total number of chunks.
    const bool _corner_mask;
    const LineType _line_type;
    const FillType _fill_type;
    const Interp _interp;

    CacheItem* _cache;

    // Current contouring operation.
    bool _filled;
    double _lower_level, _upper_level;

    // Current contouring operation, based on return type and filled or lines.
    bool _identify_holes;
    bool _combined_points;
    unsigned int _return_list_count;
};

#endif // CONTOURPY_BASE_H
