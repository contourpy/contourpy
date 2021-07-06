from contourpy import contour_generator
from contourpy.util.data import random_uniform
from contourpy.util.mpl_renderer import MplTestRenderer
import numpy as np
from .util_bench import corner_masks, fill_types, problem_sizes


class BenchFillTypeRender:
    params = (corner_masks(), fill_types(), problem_sizes())
    param_names = ["corner_mask", "fill_type", "n"]

    def setup(self, corner_mask, fill_type, n):
        self.x, self.y, self.z = random_uniform((n, n), mask_fraction=0.05)
        if corner_mask == "no mask":
            self.z = np.ma.getdata(self.z)
        self.levels = np.arange(0.0, 1.01, 0.1)

    def time_fill_type_render(self, corner_mask, fill_type, n):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name="serial", fill_type=fill_type, corner_mask=corner_mask)
        renderer = MplTestRenderer(self.x, self.y)
        for i in range(len(self.levels)-1):
            filled = cont_gen.filled(self.levels[i], self.levels[i+1])
            renderer.filled(filled, fill_type, color=f"C{i}")
        renderer.save(f"fill_type_render_{corner_mask}_{fill_type}_{n}.png")
