#include "base_impl.h"
#include "serial.h"

SerialContourGenerator::SerialContourGenerator(
    const CoordinateArray& x, const CoordinateArray& y, const CoordinateArray& z,
    const MaskArray& mask, bool corner_mask, LineType line_type, FillType fill_type, Interp interp,
    index_t x_chunk_size, index_t y_chunk_size)
    : BaseContourGenerator(x, y, z, mask, corner_mask, line_type, fill_type, interp, x_chunk_size,
                           y_chunk_size)
{}

void SerialContourGenerator::init_cache_levels_and_starts(const ChunkLocal& local)
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
        ZLevel z_nw = (istart > 0) ? Z_NW : 0;
        ZLevel z_sw = (istart > 0 && j > 0) ? Z_SW : 0;

        for (index_t i = istart; i <= iend; ++i, ++quad, ++z_ptr) {
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

            // z-level of SE point already calculated if j > 0; not needed
            // if j == 0.
            ZLevel z_se = (j > 0) ? Z_SE : 0;

            if (EXISTS_ANY(quad)) {
                if (_filled) {
                    if (EXISTS_N_AND_E_EDGES(quad)) {
                        if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw == 0 || SADDLE_Z_LEVEL(quad) == 0)) {
                            _cache[quad] |= MASK_START_N;  // N to E low.
                            start_in_row = true;
                        }
                        else if (z_nw == 2 && z_se == 2 && z_ne < 2 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw == 2 ||
                                  SADDLE_Z_LEVEL(quad) == 2)) {
                            _cache[quad] |= MASK_START_N;  // N to E high.
                            start_in_row = true;
                        }

                        if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                            _cache[quad] |= MASK_START_E;  // E to N low.
                            start_in_row = true;
                        }
                        else if (z_ne == 2 && z_nw < 2 && z_se < 2 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw < 2 || SADDLE_Z_LEVEL(quad) < 2)) {
                            _cache[quad] |= MASK_START_E;  // E to N high.
                            start_in_row = true;
                        }
                    }

                    if (BOUNDARY_S(quad) &&
                        ((z_sw == 2 && z_se < 2) || (z_sw == 0 && z_se > 0) || z_sw == 1)) {
                        _cache[quad] |= MASK_START_BOUNDARY_S;
                        start_in_row = true;
                    }

                    if (BOUNDARY_W(quad) &&
                        ((z_nw == 2 && z_sw < 2) || (z_nw == 0 && z_sw > 0) ||
                         (z_nw == 1 && (z_sw != 1 || EXISTS_NW_CORNER(quad))))) {
                        _cache[quad] |= MASK_START_BOUNDARY_W;
                        start_in_row = true;
                    }

                    if (EXISTS_ANY_CORNER(quad)) {
                        if (EXISTS_NE_CORNER(quad) &&
                            ((z_nw == 2 && z_se < 2) || (z_nw == 0 && z_se > 0) || z_nw == 1)) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                        else if (EXISTS_NW_CORNER(quad) &&
                                 ((z_sw == 2 && z_ne < 2) || (z_sw == 0 && z_ne > 0))) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                        else if (EXISTS_SE_CORNER(quad) && ((z_sw == 0 && z_se == 0 && z_ne > 0) ||
                                                            (z_sw == 2 && z_se == 2 && z_ne < 2))) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                        else if (EXISTS_SW_CORNER(quad) && z_nw == 1 && z_se == 1) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                    }

                    // Start following N boundary from E to W which is a hole.
                    // Required for an internal masked region which is a hole in
                    // a filled polygon.
                    if (BOUNDARY_N(quad) && EXISTS_N_EDGE(quad) && z_nw == 1 && z_ne == 1 &&
                        !START_HOLE_N(quad-1) && j % _y_chunk_size != 0 && j != _ny-1) {
                        _cache[quad] |= MASK_START_HOLE_N;
                        start_in_row = true;
                    }
                }
                else {  // !_filled
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

                    if (EXISTS_N_AND_E_EDGES(quad) && !BOUNDARY_N(quad) && !BOUNDARY_E(quad)) {
                        if (z_ne == 0 && z_nw > 0 && z_se > 0 &&
                            (EXISTS_NE_CORNER(quad) || z_sw > 0 || SADDLE_Z_LEVEL(quad) > 0)) {
                            _cache[quad] |= MASK_START_E;  // E to N low.
                            start_in_row = true;
                        }
                        else if (z_nw == 0 && z_se == 0 && z_ne > 0 &&
                                 (EXISTS_NE_CORNER(quad) || z_sw == 0 ||
                                  SADDLE_Z_LEVEL(quad) == 0)) {
                            _cache[quad] |= MASK_START_N;  // N to E low.
                            start_in_row = true;
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

                        if (corner_start) {
                            _cache[quad] |= MASK_START_CORNER;
                            start_in_row = true;
                        }
                    }
                }
            }

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

void SerialContourGenerator::march(std::vector<py::list>& return_lists)
{
    // Initialise cache z-levels and starting locations.
    ChunkLocal local;
    for (index_t chunk = 0; chunk < _n_chunks; ++chunk) {
        get_chunk_limits(chunk, local);
        init_cache_levels_and_starts(local);
        local.clear();
    }

    // Trace contours.
    for (index_t chunk = 0; chunk < _n_chunks; ++chunk) {
        get_chunk_limits(chunk, local);
        if (_filled)
            march_chunk_filled(local, return_lists);
        else
            march_chunk_lines(local, return_lists);
        local.clear();
    }
}
