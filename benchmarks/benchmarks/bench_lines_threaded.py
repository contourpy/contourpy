from contourpy import contour_generator, LineType
from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, problem_sizes, thread_counts


class BenchLinesThreaded(BenchBase):
    params = (
        ["threaded"], datasets(), [LineType.ChunkCombinedOffsets], corner_masks(), problem_sizes(),
        [40], thread_counts())
    param_names = (
        "name", "dataset", "line_type", "corner_mask", "n", "chunk_count", "thread_count")

    def setup(self, name, dataset, line_type, corner_mask, n, chunk_count, thread_count):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_lines_threaded(
        self, name, dataset, line_type, corner_mask, n, chunk_count, thread_count):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
             self.x, self.y, self.z, name=name, line_type=line_type, corner_mask=corner_mask,
            chunk_count=chunk_count, thread_count=thread_count)
        for level in self.levels:
            cont_gen.lines(level)
