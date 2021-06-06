from contourpy import contour_generator, FillType
from contourpy.util.data import random_uniform
import numpy as np
from .util_bench import corner_masks, problem_sizes, thread_counts

class BenchFilledThreaded:
    params = (thread_counts(), corner_masks(), problem_sizes())
    param_names = ['thread_count', 'corner_mask', 'n']

    def setup(self, thread_count, corner_mask, n):
        self.x, self.y, self.z = random_uniform((n, n), mask_fraction=0.05)
        if corner_mask == 'no mask':
            self.z = np.ma.getdata(self.z)
        self.levels = np.arange(0.0, 1.01, 0.1)

    def time_filled_threaded(self, thread_count, corner_mask, n):
        cont_gen = contour_generator(
            self.x, self.y, self.z, name='threaded', thread_count=thread_count,
            chunk_count=24, fill_type=FillType.ChunkCombinedOffsets2,
            corner_mask=corner_mask if corner_mask != 'no mask' else False)
        all_filled = [cont_gen.filled(lower, upper) for lower, upper in
                      zip(self.levels[:-1], self.levels[1:])]
