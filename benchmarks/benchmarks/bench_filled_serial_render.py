from __future__ import annotations

from contourpy import FillType, contour_generator
from contourpy.util.mpl_renderer import MplTestRenderer

from .bench_base import BenchBase
from .util_bench import corner_mask_to_bool, corner_masks, datasets, fill_types, problem_sizes


class BenchFilledSerialRender(BenchBase):
    params: tuple[list[str], list[str], list[FillType], list[str | bool], list[int]] = (
        ["serial"], datasets(), fill_types(), corner_masks(), problem_sizes(),
    )
    param_names: tuple[str, ...] = ("name", "dataset", "fill_type", "corner_mask", "n")

    def setup(
        self, name: str, dataset: str, fill_type: FillType, corner_mask: str | bool, n: int,
    ) -> None:
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_serial_render(
        self, name: str, dataset: str, fill_type: FillType, corner_mask: str | bool, n: int,
    ) -> None:
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type,
            corner_mask=corner_mask_to_bool(corner_mask),
        )
        renderer = MplTestRenderer()
        for i in range(len(self.levels)-1):
            filled = cont_gen.filled(self.levels[i], self.levels[i+1])
            renderer.filled(filled, fill_type, color=f"C{i}")
        renderer.save(f"filled_{name}_{corner_mask}_{fill_type}_{n}.png")
