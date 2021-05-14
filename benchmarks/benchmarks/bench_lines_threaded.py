from contourpy import contour_generator, LineType
from contourpy.util import random_uniform
import numpy as np
from .util_bench import corner_masks, problem_sizes, thread_counts

class BenchLinesThreaded:
    params = (thread_counts(), corner_masks(), problem_sizes())
    param_names = ['thread_count', 'corner_mask', 'n']

    def setup(self, thread_count, corner_mask, n):
        self.x, self.y, self.z = random_uniform((n, n), mask_fraction=0.05)
        if corner_mask == 'no mask':
            self.z = np.ma.getdata(self.z)
        self.levels = np.arange(0.0, 1.01, 0.1)

    def time_lines_threaded(self, thread_count, corner_mask, n):
        cont_gen = contour_generator(
            self.x, self.y, self.z, name='threaded', thread_count=thread_count,
            chunk_count=24, line_type=LineType.ChunkCombinedOffsets,
            corner_mask=corner_mask if corner_mask != 'no mask' else False)
        all_lines = [cont_gen.lines(level) for level in self.levels]
