from contourpy import LineType, contour_generator

from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, line_types, problem_sizes, thread_counts


class BenchLinesThreaded(BenchBase):
    params = (
        ["threaded"], datasets(), line_types(), corner_masks(), problem_sizes(), [40],
        thread_counts())
    param_names = (
        "name", "dataset", "line_type", "corner_mask", "n", "total_chunk_count", "thread_count")

    def setup(self, name, dataset, line_type, corner_mask, n, total_chunk_count, thread_count):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_lines_threaded(
            self, name, dataset, line_type, corner_mask, n, total_chunk_count, thread_count):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, line_type=line_type, corner_mask=corner_mask,
            total_chunk_count=total_chunk_count, thread_count=thread_count)
        for level in self.levels:
            cont_gen.lines(level)
