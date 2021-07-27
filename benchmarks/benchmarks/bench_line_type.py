from contourpy import contour_generator
from contourpy.util.data import random
import numpy as np
from .util_bench import corner_masks, line_types, problem_sizes


class BenchLineType:
    params = (corner_masks(), line_types(), problem_sizes())
    param_names = ["corner_mask", "line_type", "n"]

    def setup(self, corner_mask, line_type, n):
        self.x, self.y, self.z = random((n, n), mask_fraction=0.05)
        if corner_mask == "no mask":
            self.z = np.ma.getdata(self.z)
        self.levels = np.arange(0.0, 1.01, 0.1)

    def time_line_type(self, corner_mask, line_type, n):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name="serial", line_type=line_type, corner_mask=corner_mask)
        for level in self.levels:
            cont_gen.lines(level)
