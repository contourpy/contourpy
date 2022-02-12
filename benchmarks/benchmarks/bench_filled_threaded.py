from contourpy import contour_generator, FillType
from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, problem_sizes, thread_counts


class BenchFilledThreaded(BenchBase):
    params = (
        ["threaded"], datasets(), [FillType.ChunkCombinedOffsetOffset], corner_masks(), problem_sizes(),
        [40], thread_counts())
    param_names = (
        "name", "dataset", "fill_type", "corner_mask", "n", "chunk_count", "thread_count")

    def setup(self, name, dataset, fill_type, corner_mask, n, chunk_count, thread_count):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_threaded(
        self, name, dataset, fill_type, corner_mask, n, chunk_count, thread_count):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type, corner_mask=corner_mask,
            chunk_count=chunk_count, thread_count=thread_count)
        for i in range(len(self.levels)-1):
            cont_gen.filled(self.levels[i], self.levels[i+1])
