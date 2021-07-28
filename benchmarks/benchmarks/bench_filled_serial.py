from contourpy import contour_generator
from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, fill_types, problem_sizes


class BenchFilledSerial(BenchBase):
    params = (["serial"], datasets(), fill_types(), corner_masks(), problem_sizes())
    param_names = ("name", "dataset", "fill_type", "corner_mask", "n")

    def setup(self, name, dataset, fill_type, corner_mask, n):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_serial(self, name, dataset, fill_type, corner_mask, n):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type, corner_mask=corner_mask)
        for i in range(len(self.levels)-1):
            cont_gen.filled(self.levels[i], self.levels[i+1])
