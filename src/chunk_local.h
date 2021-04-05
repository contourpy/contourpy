#ifndef CONTOURPY_CHUNK_LOCAL_H
#define CONTOURPY_CHUNK_LOCAL_H

#include <iosfwd>
#include <vector>

struct ChunkLocal
{
    ChunkLocal();

    void clear();

    friend std::ostream &operator<<(std::ostream &os, const ChunkLocal& local);



    long chunk;                       // Index in range 0 to _n_chunks-1.

    long istart, iend, jstart, jend;  // Chunk limits.
    int pass;
    double* points;                   // Where to store next point.

    // Data for whole pass.
    unsigned long total_point_count;
    unsigned long line_count;                  // Total of all lines
    unsigned long hole_count;                  // Holes only.
    std::vector<unsigned long> line_offsets;   // Into array of all points.
    std::vector<unsigned long> outer_offsets;  // Into array of line offsets.

    // Data for current outer.
    std::vector<long> look_up_quads;  // To find holes of current outer.
};

#endif // CONTOURPY_CHUNK_LOCAL_H
