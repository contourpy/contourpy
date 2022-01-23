from contourpy import contour_generator, FillType, LineType
from contourpy.util.data import random
from contourpy.util.mpl_renderer import MplRenderer
from image_comparison import compare_images
import numpy as np
import pytest

try:
    from contourpy.util.bokeh_renderer import BokehRenderer
except:
    BokehRenderer = None


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize(
    "renderer_class, renderer_name", [(MplRenderer, "mpl"), (BokehRenderer, "bokeh")])
def test_renderer_filled(fill_type, renderer_class, renderer_name):
    if renderer_class is None:
        pytest.skip()
    x, y, z = random((3, 4))
    renderer = renderer_class(ncols=2, figsize=(8, 3), show_frame=False)
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
    compare_images(image_buffer, f"renderer_filled_{renderer_name}.png", f"{fill_type}")


@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize(
    "renderer_class, renderer_name", [(MplRenderer, "mpl"), (BokehRenderer, "bokeh")])
def test_renderer_lines(line_type, renderer_class, renderer_name):
    if renderer_class is None:
        pytest.skip()
    x, y, z = random((3, 4))
    renderer = renderer_class(ncols=2, figsize=(8, 3))
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
    compare_images(image_buffer, f"renderer_lines_{renderer_name}.png", f"{line_type}")
