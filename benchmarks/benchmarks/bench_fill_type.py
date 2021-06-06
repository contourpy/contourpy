from contourpy import contour_generator
from contourpy.util.data import random_uniform
import numpy as np
from .util_bench import corner_masks, fill_types, problem_sizes

class BenchFillType:
    params = (corner_masks(), fill_types(), problem_sizes())
    param_names = ['corner_mask', 'fill_type', 'n']

    def setup(self, corner_mask, fill_type, n):
        self.x, self.y, self.z = random_uniform((n, n), mask_fraction=0.05)
        if corner_mask == 'no mask':
            self.z = np.ma.getdata(self.z)
        self.levels = np.arange(0.0, 1.01, 0.1)

    def time_fill_type(self, corner_mask, fill_type, n):
        cont_gen = contour_generator(
            self.x, self.y, self.z, name='serial', fill_type=fill_type,
            corner_mask=corner_mask if corner_mask != 'no mask' else False)
        all_filled = [cont_gen.filled(lower, upper) for lower, upper in
                      zip(self.levels[:-1], self.levels[1:])]
