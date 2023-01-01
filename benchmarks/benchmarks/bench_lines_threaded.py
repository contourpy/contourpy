from __future__ import annotations

from contourpy import LineType, contour_generator

from .bench_base import BenchBase
from .util_bench import (
    corner_mask_to_bool, corner_masks, datasets, line_types, problem_sizes, thread_counts,
)


class BenchLinesThreaded(BenchBase):
    params: tuple[list[str], list[str], list[LineType], list[str | bool], list[int], list[int],
                  list[int]] = (
        ["threaded"], datasets(), line_types(), corner_masks(), problem_sizes(), [40],
        thread_counts(),
    )
    param_names: tuple[str, ...] = (
        "name", "dataset", "line_type", "corner_mask", "n", "total_chunk_count", "thread_count",
    )

    def setup(
        self, name: str, dataset: str, line_type: LineType, corner_mask: str | bool, n: int,
        total_chunk_count: int, thread_count: int,
    ) -> None:
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_lines_threaded(
        self, name: str, dataset: str, line_type: LineType, corner_mask: str | bool, n: int,
        total_chunk_count: int, thread_count: int,
    ) -> None:
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, line_type=line_type,
            corner_mask=corner_mask_to_bool(corner_mask), total_chunk_count=total_chunk_count,
            thread_count=thread_count,
        )
        for level in self.levels:
            cont_gen.lines(level)
