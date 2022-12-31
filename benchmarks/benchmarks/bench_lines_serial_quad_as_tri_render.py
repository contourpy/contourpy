from __future__ import annotations

from contourpy import LineType, contour_generator
from contourpy.util.mpl_renderer import MplTestRenderer

from .bench_base import BenchBase
from .util_bench import corner_mask_to_bool, corner_masks, datasets, problem_sizes


class BenchLinesSerialQuadAsTriRender(BenchBase):
    params: tuple[list[str], list[str], list[LineType], list[str | bool], list[int]] = (
        ["serial"], datasets(), [LineType.SeparateCode], corner_masks(), problem_sizes(),
    )
    param_names: tuple[str, ...] = ("name", "dataset", "line_type", "corner_mask", "n")

    def setup(
        self, name: str, dataset: str, line_type: LineType, corner_mask: str | bool, n: int,
    ) -> None:
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_lines_serial_quad_as_tri_render(
        self, name: str, dataset: str, line_type: LineType, corner_mask: str | bool, n: int,
    ) -> None:
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, line_type=line_type,
            corner_mask=corner_mask_to_bool(corner_mask), quad_as_tri=True,
        )
        renderer = MplTestRenderer()
        for i, level in enumerate(self.levels):
            lines = cont_gen.lines(level)
            renderer.lines(lines, line_type, color=f"C{i}")
        renderer.save(f"lines_{name}_{corner_mask}_{line_type}_{n}_True.png")
