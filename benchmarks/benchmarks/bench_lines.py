from contourpy import contour_generator, LineType
from contourpy.util.data import random_uniform
import numpy as np
from .util_bench import corner_masks, problem_sizes

class BenchFilled:
    params = (['mpl2005', 'mpl2014', 'serial'], corner_masks(), problem_sizes())
    param_names = ['name', 'corner_mask', 'n']

    def setup(self, name, corner_mask, n):
        self.x, self.y, self.z = random_uniform((n, n), mask_fraction=0.05)
        if corner_mask == 'no mask':
            self.z = np.ma.getdata(self.z)
        self.levels = np.arange(0.0, 1.01, 0.1)

    def time_lines(self, name, corner_mask, n):
        if name == 'mpl2005' and corner_mask == True:
            raise NotImplementedError  # Does not support corner_mask=True
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, line_type=LineType.SeparateCodes,
            corner_mask=corner_mask if corner_mask != 'no mask' else False)
        all_lines = [cont_gen.lines(level) for level in self.levels]
        