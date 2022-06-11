from contourpy import contour_generator
from contourpy.util.mpl_renderer import MplTestRenderer

from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, line_types, problem_sizes


class BenchLinesSerialRender(BenchBase):
    params = (["serial"], datasets(), line_types(), corner_masks(), problem_sizes())
    param_names = ("name", "dataset", "line_type", "corner_mask", "n")

    def setup(self, name, dataset, line_type, corner_mask, n):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_lines_serial_render(self, name, dataset, line_type, corner_mask, n):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, line_type=line_type, corner_mask=corner_mask)
        renderer = MplTestRenderer()
        for i, level in enumerate(self.levels):
            lines = cont_gen.lines(level)
            renderer.lines(lines, line_type, color=f"C{i}")
        renderer.save(f"lines_{name}_{corner_mask}_{line_type}_{n}.png")
