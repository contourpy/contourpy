from contourpy import contour_generator, FillType
from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, problem_sizes


class BenchFilledSerialQuadAsTri(BenchBase):
    params = (["serial"], datasets(), [FillType.OuterCode], corner_masks(), problem_sizes())
    param_names = ("name", "dataset", "fill_type", "corner_mask", "n")

    def setup(self, name, dataset, fill_type, corner_mask, n):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_serial_quad_as_tri(self, name, dataset, fill_type, corner_mask, n):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type, corner_mask=corner_mask,
            quad_as_tri=True)
        for i in range(len(self.levels)-1):
            cont_gen.filled(self.levels[i], self.levels[i+1])
