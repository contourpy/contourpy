from contourpy import contour_generator, LineType
from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, problem_sizes


class BenchLinesSerialQuadAsTri(BenchBase):
    params = (["serial"], datasets(), [LineType.SeparateCode], corner_masks(), problem_sizes())
    param_names = ("name", "dataset", "line_type", "corner_mask", "n")

    def setup(self, name, dataset, line_type, corner_mask, n):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_lines_serial_quad_as_tri(self, name, dataset, line_type, corner_mask, n):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, line_type=line_type, corner_mask=corner_mask,
            quad_as_tri=True)
        for level in self.levels:
            cont_gen.lines(level)
