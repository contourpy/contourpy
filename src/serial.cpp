#include "base_impl.h"
#include "converter.h"
#include "serial.h"

namespace contourpy {

SerialContourGenerator::SerialContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
    const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type,
    bool quad_as_tri, ZInterp z_interp, index_t x_chunk_size, index_t y_chunk_size)
    : BaseContourGenerator(x, y, z, mask, corner_mask, line_type, fill_type, quad_as_tri, z_interp,
                           x_chunk_size, y_chunk_size)
{}

void SerialContourGenerator::export_lines(ChunkLocal& local, std::vector<py::list>& return_lists)
{
    assert(local.total_point_count > 0);

    switch (get_line_type())
    {
        case LineType::Separate:
        case LineType::SeparateCode: {
            assert(!_direct_points && !_direct_line_offsets);

            bool separate_code = (get_line_type() == LineType::SeparateCode);

            for (decltype(local.line_count) i = 0; i < local.line_count; ++i) {
                auto point_start = local.line_offsets.start[i];
                auto point_end = local.line_offsets.start[i+1];
                auto point_count = point_end - point_start;
                assert(point_count > 1);

                return_lists[0].append(Converter::convert_points(
                    point_count, local.points.start + 2*point_start));

                if (separate_code) {
                    return_lists[1].append(
                        Converter::convert_codes_check_closed_single(
                            point_count, local.points.start + 2*point_start));
                }
            }
            break;
        }
        case LineType::ChunkCombinedCode: {
            assert(_direct_points && !_direct_line_offsets);

            // return_lists[0][local.chunk] already contains points.
            return_lists[1][local.chunk] = Converter::convert_codes_check_closed(
                local.total_point_count, local.line_count + 1, local.line_offsets.start,
                local.points.start);
            break;
        }
        case LineType::ChunkCombinedOffset:
            assert(_direct_points && _direct_line_offsets);
            // return_lists[0][local.chunk] already contains points.
            // return_lists[1][local.chunk] already contains line offsets.
            break;
    }
}

void SerialContourGenerator::march(std::vector<py::list>& return_lists)
{
    // Stage 1: Initialise cache z-levels and starting locations for whole domain.
    init_cache_levels_and_starts();

    // Stage 2: Trace contours.
    auto n_chunks = get_n_chunks();
    ChunkLocal local;
    for (index_t chunk = 0; chunk < n_chunks; ++chunk) {
        get_chunk_limits(chunk, local);
        march_chunk(local, return_lists);
        local.clear();
    }
}

} // namespace contourpy
