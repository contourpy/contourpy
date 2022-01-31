import numpy as np
import pytest

from contourpy import contour_generator, FillType, LineType
from contourpy.util.data import random
from contourpy.util.mpl_renderer import MplRenderer
from image_comparison import compare_images


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
def test_renderer_filled(fill_type):
    x, y, z = random((3, 4))
    renderer = MplRenderer(ncols=2, figsize=(8, 3), show_frame=False)
    for ax, quad_as_tri in enumerate((False, True)):
        cont_gen = contour_generator(x, y, z, fill_type=fill_type)

        levels = np.linspace(0.0, 1.0, 11)
        for i in range(len(levels)-1):
            filled = cont_gen.filled(levels[i], levels[i+1])
            if quad_as_tri:
                renderer.filled(filled, fill_type, ax=ax, color=f"C{i}", alpha=0.4)
            else:
                renderer.filled(filled, fill_type, ax=ax, color=f"C{i}")

        if quad_as_tri:
            renderer.grid(x, y, ax=ax, alpha=0.5, quad_as_tri_alpha=0.5)
            renderer.title("Title", ax=ax)
        else:
            renderer.grid(x, y, ax=ax, alpha=0.8, point_color="black")
            renderer.title("Colored title", ax=ax, color="red")

    image_buffer = renderer.save_to_buffer()
    compare_images(image_buffer, "renderer_filled_mpl.png", f"{fill_type}")


@pytest.mark.parametrize("line_type", LineType.__members__.values())
def test_renderer_lines(line_type):
    x, y, z = random((3, 4))
    renderer = MplRenderer(ncols=2, figsize=(8, 3))
    for ax, quad_as_tri in enumerate((False, True)):
        cont_gen = contour_generator(x, y, z, line_type=line_type)

        levels = np.linspace(0.1, 0.9, 9)
        for i in range(len(levels)):
            lines = cont_gen.lines(levels[i])
            if quad_as_tri:
                renderer.lines(lines, line_type, ax=ax, color=f"C{i}", alpha=0.5, linewidth=3)
            else:
                renderer.lines(lines, line_type, ax=ax, color=f"C{i}")

        if quad_as_tri:
            renderer.grid(x, y, ax=ax, alpha=0.2, quad_as_tri_alpha=0.2)
            renderer.z_values(x, y, z, ax=ax, fmt=".2f", quad_as_tri=True)
            renderer.title("Title", ax=ax)
        else:
            renderer.grid(x, y, ax=ax, point_color="black")
            renderer.z_values(x, y, z, ax=ax, fmt=".2f", color="blue")
            renderer.title("Colored title", ax=ax, color="red")

    image_buffer = renderer.save_to_buffer()
    compare_images(image_buffer, "renderer_lines_mpl.png", f"{line_type}")
