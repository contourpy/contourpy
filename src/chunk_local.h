#ifndef CONTOURPY_CHUNK_LOCAL_H
#define CONTOURPY_CHUNK_LOCAL_H

#include "common.h"
#include <iosfwd>
#include <vector>

struct ChunkLocal
{
    ChunkLocal();

    void clear();

    friend std::ostream &operator<<(std::ostream &os, const ChunkLocal& local);



    index_t chunk;                       // Index in range 0 to _n_chunks-1.
    index_t istart, iend, jstart, jend;  // Chunk limits, inclusive.
    int pass;
    double* points;                      // Where to store next point.

    // Data for whole pass.
    count_t total_point_count;
    count_t line_count;                  // Count of all lines
    count_t hole_count;                  // Count of holes only.
    std::vector<offset_t> line_offsets;  // Into array of all points.
    std::vector<offset_t> outer_offsets; // Into array of line offsets.

    // Data for current outer.
    std::vector<index_t> look_up_quads;  // To find holes of current outer.
};

#endif // CONTOURPY_CHUNK_LOCAL_H
