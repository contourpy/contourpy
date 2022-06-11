from contourpy import FillType, contour_generator
from contourpy.util.mpl_renderer import MplTestRenderer

from .bench_base import BenchBase
from .util_bench import corner_masks, datasets, problem_sizes


class BenchFilledMpl20xxRender(BenchBase):
    params = (
        ["mpl2005", "mpl2014"], datasets(), [FillType.OuterCode], corner_masks(), problem_sizes())
    param_names = ("name", "dataset", "fill_type", "corner_mask", "n")

    def setup(self, name, dataset, fill_type, corner_mask, n):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_mpl20xx_render(self, name, dataset, fill_type, corner_mask, n):
        if name == "mpl2005" and corner_mask is True:
            raise NotImplementedError  # Does not support corner_mask=True
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type, corner_mask=corner_mask)
        renderer = MplTestRenderer()
        for i in range(len(self.levels)-1):
            filled = cont_gen.filled(self.levels[i], self.levels[i+1])
            renderer.filled(filled, fill_type, color=f"C{i}")
        renderer.save(f"filled_{name}_{corner_mask}_{fill_type}_{n}.png")
