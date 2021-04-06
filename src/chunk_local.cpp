#include "chunk_local.h"
#include <iostream>

ChunkLocal::ChunkLocal()
{
    line_offsets.reserve(100);
    outer_offsets.reserve(100);
    look_up_quads.reserve(100);
    clear();
}

void ChunkLocal::clear()
{
    chunk = -1;
    istart = iend = jstart = jend = -1;
    pass = -1;
    points = nullptr;

    total_point_count = 0;
    line_count = 0;
    hole_count = 0;
    line_offsets.clear();
    outer_offsets.clear();
}

std::ostream &operator<<(std::ostream &os, const ChunkLocal& local)
{
    os << "ChunkLocal:"
        << " chunk=" << local.chunk
        << " istart=" << local.istart
        << " iend=" << local.iend
        << " jstart=" << local.jstart
        << " jend=" << local.jend
        << " total_point_count=" << local.total_point_count
        << " line_count=" << local.line_count
        << " hole_count=" << local.hole_count;

    os << " line_offsets(" << local.line_offsets.size() << ")";
    if (!local.line_offsets.empty()) {
        os << "=";
        for (auto count : local.line_offsets)
            os << count << " ";
    }

    os << " outer_offsets(" << local.outer_offsets.size() << ")";
    if (!local.outer_offsets.empty()) {
        os << "=";
        for (auto count : local.outer_offsets)
            os << count << " ";
    }

    return os;
}
