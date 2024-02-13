from __future__ import annotations

from asv_runner.benchmarks.mark import SkipNotImplemented

from contourpy import FillType, contour_generator
from contourpy.util.mpl_renderer import MplTestRenderer

from .bench_base import BenchBase
from .util_bench import corner_mask_to_bool, corner_masks, datasets, problem_sizes


class BenchFilledMpl20xxRender(BenchBase):
    params: tuple[list[str], list[str], list[FillType], list[str | bool], list[int]] = (
        ["mpl2005", "mpl2014"], datasets(), [FillType.OuterCode], corner_masks(), problem_sizes(),
    )
    param_names: tuple[str, ...] = ("name", "dataset", "fill_type", "corner_mask", "n")

    def setup(
        self, name: str, dataset: str, fill_type: FillType, corner_mask: str | bool, n: int,
    ) -> None:
        if name == "mpl2005" and corner_mask is True:
            raise SkipNotImplemented(f"{name} does not support corner_mask={corner_mask}")
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_mpl20xx_render(
        self, name: str, dataset: str, fill_type: FillType, corner_mask: str | bool, n: int,
    ) -> None:
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type,
            corner_mask=corner_mask_to_bool(corner_mask),
        )
        renderer = MplTestRenderer()
        renderer.multi_filled(cont_gen.multi_filled(self.levels), fill_type)
        renderer.save(f"filled_{name}_{corner_mask}_{fill_type}_{n}.png")
