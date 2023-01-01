from __future__ import annotations

from contourpy import FillType, contour_generator

from .bench_base import BenchBase
from .util_bench import corner_mask_to_bool, corner_masks, datasets, problem_sizes


class BenchFilledMpl20xx(BenchBase):
    params: tuple[list[str], list[str], list[FillType], list[str | bool], list[int]] = (
        ["mpl2005", "mpl2014"], datasets(), [FillType.OuterCode], corner_masks(), problem_sizes(),
    )
    param_names: tuple[str, ...] = ("name", "dataset", "fill_type", "corner_mask", "n")

    def setup(
        self, name: str, dataset: str, fill_type: FillType, corner_mask: str | bool, n: int,
    ) -> None:
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_mpl20xx(
        self, name: str, dataset: str, fill_type: FillType, corner_mask: str | bool, n: int,
    ) -> None:
        if name == "mpl2005" and corner_mask is True:
            raise NotImplementedError  # Does not support corner_mask=True
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type,
            corner_mask=corner_mask_to_bool(corner_mask),
        )
        for i in range(len(self.levels)-1):
            cont_gen.filled(self.levels[i], self.levels[i+1])
