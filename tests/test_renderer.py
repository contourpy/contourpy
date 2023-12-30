from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import numpy as np
import pytest

from contourpy import FillType, LineType, contour_generator
from contourpy.util.data import random, simple

if TYPE_CHECKING:
    from _pytest._py.path import LocalPath


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("fill_type", [*FillType.__members__.values(), "OuterCode"])
@pytest.mark.parametrize("multi", [False, True])
def test_debug_renderer_filled(show_text: bool, fill_type: FillType | str, multi: bool) -> None:
    from contourpy.util.mpl_renderer import MplDebugRenderer

    from .image_comparison import compare_images

    renderer = MplDebugRenderer(figsize=(4.5, 3), show_frame=show_text)
    x, y, z = simple((3, 4))
    z[0, 2] = 0  # Ensure empty chunk
    cont_gen = contour_generator(x, y, z, fill_type=fill_type, chunk_size=2)
    levels = [0.25, 0.6]

    if multi:
        multi_filled = cont_gen.multi_filled(levels)
        renderer.multi_filled(multi_filled, fill_type, color="C1")
    else:
        filled = cont_gen.filled(levels[0], levels[1])
        renderer.filled(filled, fill_type, color="C1")

    renderer.grid(x, y)
    if show_text:
        renderer.quad_numbers(x, y, z)
        renderer.z_levels(x, y, z, lower_level=levels[0], upper_level=levels[1])

    image_buffer = renderer.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"debug_renderer_filled{suffix}.png", f"{fill_type}_{multi}")


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("line_type", [*LineType.__members__.values(), "Separate"])
@pytest.mark.parametrize("multi", [False, True])
def test_debug_renderer_lines(show_text: bool, line_type: LineType, multi: bool) -> None:
    from contourpy.util.mpl_renderer import MplDebugRenderer

    from .image_comparison import compare_images

    renderer = MplDebugRenderer(figsize=(4.5, 3), show_frame=show_text)
    x, y, z = simple((3, 4))
    cont_gen = contour_generator(x, y, z, line_type=line_type)
    levels = [0.25, 0.6]

    if multi:
        multi_lines = cont_gen.multi_lines(levels)
        renderer.multi_lines(multi_lines, line_type, linewidth=2)
    else:
        for i, level in enumerate(levels):
            lines = cont_gen.lines(level)
            renderer.lines(lines, line_type, color=f"C{i}", linewidth=2)

    renderer.grid(x, y)
    if show_text:
        renderer.quad_numbers(x, y, z)
        renderer.point_numbers(x, y, z)

    image_buffer = renderer.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"debug_renderer_lines{suffix}.png", f"{line_type}_{multi}")


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("debug", [False, True])
@pytest.mark.parametrize("fill_type", [*FillType.__members__.values(), "OuterCode"])
@pytest.mark.parametrize("multi", [False, True])
def test_renderer_filled(show_text: bool, debug: bool, fill_type: FillType, multi: bool) -> None:
    from contourpy.util.mpl_renderer import MplDebugRenderer, MplRenderer

    from .image_comparison import compare_images

    # Same results from MplDebugRenderer if extra kwargs supplied to renderer.Filled() call.
    filled_kw: dict[str, Any] = {"line_color": None, "point_color": None} if debug else {}
    filled_quad_as_tri_kw = filled_kw.copy() | {"alpha": 0.4}

    if not debug:
        renderer = MplRenderer(ncols=2, figsize=(8, 3), show_frame=False)
    else:
        renderer = MplDebugRenderer(ncols=2, figsize=(8, 3), show_frame=False)

    x, y, z = random((3, 4), mask_fraction=0.35)
    for ax, quad_as_tri in enumerate((False, True)):
        cont_gen = contour_generator(x, y, z, fill_type=fill_type)
        kwargs = filled_quad_as_tri_kw if quad_as_tri else filled_kw

        levels = np.linspace(0.0, 1.0, 11)
        if multi:
            multi_filled = cont_gen.multi_filled(levels)
            renderer.multi_filled(multi_filled, fill_type, ax=ax, **kwargs)
        else:
            for i in range(len(levels)-1):
                filled = cont_gen.filled(levels[i], levels[i+1])
                renderer.filled(filled, fill_type, ax=ax, color=f"C{i}", **kwargs)

        if quad_as_tri:
            renderer.grid(x, y, ax=ax, alpha=0.5, quad_as_tri_alpha=0.5)
            renderer.mask(x, y, z, ax=ax, color="red")
            if show_text:
                renderer.title("Title", ax=ax)
        else:
            renderer.grid(x, y, ax=ax, alpha=0.8, point_color="black")
            if show_text:
                renderer.title("Colored title", ax=ax, color="red")

    image_buffer = renderer.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    debug_suffix = "_debug" if debug else ""
    compare_images(
        image_buffer, f"renderer_filled{suffix}.png", f"{fill_type}{debug_suffix}_{multi}",
    )


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("debug", [False, True])
@pytest.mark.parametrize("line_type", [*LineType.__members__.values(), "Separate"])
@pytest.mark.parametrize("multi", [False, True])
def test_renderer_lines(show_text: bool, debug: bool, line_type: LineType, multi: bool) -> None:
    from contourpy.util.mpl_renderer import MplDebugRenderer, MplRenderer

    from .image_comparison import compare_images

    # Same results from MplDebugRenderer if extra kwargs supplied to renderer.lines() call.
    lines_kw: dict[str, Any] = {"arrow_size": 0, "point_color": None} if debug else {}
    lines_quad_as_tri_kw = lines_kw.copy() | {"alpha": 0.5, "linewidth": 3}

    if not debug:
        renderer = MplRenderer(ncols=2, figsize=(8, 3), show_frame=show_text)
    else:
        renderer = MplDebugRenderer(ncols=2, figsize=(8, 3), show_frame=show_text)

    x, y, z = random((3, 4), mask_fraction=0.35)
    for ax, quad_as_tri in enumerate((False, True)):
        cont_gen = contour_generator(x, y, z, line_type=line_type)
        kwargs = lines_quad_as_tri_kw if quad_as_tri else lines_kw

        levels = np.linspace(0.1, 0.9, 9)
        if multi:
            multi_lines = cont_gen.multi_lines(levels)
            renderer.multi_lines(multi_lines, line_type, ax=ax, **kwargs)
        else:
            for i in range(len(levels)):
                lines = cont_gen.lines(levels[i])
                renderer.lines(lines, line_type, ax=ax, color=f"C{i}", **kwargs)

        if quad_as_tri:
            renderer.grid(x, y, ax=ax, alpha=0.2, quad_as_tri_alpha=0.2)
            renderer.mask(x, y, z, ax=ax, color="red")
            if show_text:
                renderer.z_values(x, y, z, ax=ax, fmt=".2f", quad_as_tri=True)
                renderer.title("Title", ax=ax)
        else:
            renderer.grid(x, y, ax=ax, point_color="black")
            if show_text:
                renderer.z_values(x, y, z, ax=ax, fmt=".2f", color="blue")
                renderer.title("Colored title", ax=ax, color="red")

    image_buffer = renderer.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    debug_suffix = "_debug" if debug else ""
    compare_images(
        image_buffer, f"renderer_lines{suffix}.png", f"{line_type}{debug_suffix}_{multi}",
    )


@pytest.mark.image
@pytest.mark.parametrize("transparent", [False, True])
def test_save_png(transparent: bool, tmpdir: LocalPath) -> None:
    from PIL import Image

    from contourpy.util.mpl_renderer import MplRenderer

    renderer = MplRenderer(figsize=(4, 3))
    filename = (tmpdir / "mpl.png").strpath
    renderer.save(filename, transparent)

    # Testing that a PNG file is produced of the correct size and format.
    # Not testing the actual image produced except for the first pixel to confirm transparency.
    with Image.open(filename) as image:
        assert image.format == "PNG"
        assert image.mode == "RGBA"
        assert image.size == (400, 300)
        rgba = image.getpixel((0, 0))
        assert rgba[:3] == (255, 255, 255)
        assert rgba[3] == 0 if transparent else 255


@pytest.mark.image
@pytest.mark.parametrize("transparent", [False, True])
def test_save_svg(transparent: bool, tmpdir: LocalPath) -> None:
    from contourpy.util.mpl_renderer import MplRenderer

    renderer = MplRenderer(figsize=(4, 3))
    filename = (tmpdir / "mpl.svg").strpath
    renderer.save(filename, transparent)

    # Rather simplistic check of SVG file contents.
    with open(filename) as f:
        svg = f.read()

    assert len(re.findall("<svg ", svg)) == 1
    count0 = len(re.findall("fill: none", svg))
    count1 = len(re.findall("fill: #ffffff", svg))
    if transparent:
        assert count0 == 6 and count1 == 0
    else:
        assert count0 == 4 and count1 == 2
