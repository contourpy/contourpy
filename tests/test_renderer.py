from __future__ import annotations

import numpy as np
import pytest

from contourpy import FillType, LineType, contour_generator
from contourpy.util.data import random, simple


def test_chrome_version() -> None:
    # Print version of chrome used for export to PNG by Bokeh as test images, particularly those
    # containing text, are sensitive to chrome version.
    try:
        import contourpy.util.bokeh_renderer  # noqa: F401
    except ImportError:
        pytest.skip("Optional bokeh dependencies not installed")

    from bokeh.io.webdriver import webdriver_control
    driver = webdriver_control.get()
    capabilities = driver.capabilities
    print("chrome version used by Bokeh:", capabilities["browserVersion"])
    if "chrome" in capabilities:
        print("chromedriver version used by Bokeh:", capabilities["chrome"]["chromedriverVersion"])


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
def test_debug_renderer_filled(show_text: bool, fill_type: FillType) -> None:
    from contourpy.util.mpl_renderer import MplDebugRenderer

    from .image_comparison import compare_images

    renderer = MplDebugRenderer(figsize=(4.5, 3), show_frame=show_text)
    x, y, z = simple((3, 4))
    cont_gen = contour_generator(x, y, z, fill_type=fill_type)
    levels = [0.25, 0.6]

    filled = cont_gen.filled(levels[0], levels[1])
    renderer.filled(filled, fill_type, color="C1")

    renderer.grid(x, y)
    if show_text:
        renderer.quad_numbers(x, y, z)
        renderer.z_levels(x, y, z, lower_level=levels[0], upper_level=levels[1])

    image_buffer = renderer.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"debug_renderer_filled{suffix}.png", f"{fill_type}")


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("line_type", LineType.__members__.values())
def test_debug_renderer_lines(show_text: bool, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplDebugRenderer

    from .image_comparison import compare_images

    renderer = MplDebugRenderer(figsize=(4.5, 3), show_frame=show_text)
    x, y, z = simple((3, 4))
    cont_gen = contour_generator(x, y, z, line_type=line_type)
    levels = [0.25, 0.6]

    for i, level in enumerate(levels):
        lines = cont_gen.lines(level)
        renderer.lines(lines, line_type, color=f"C{i}", linewidth=2)

    renderer.grid(x, y)
    if show_text:
        renderer.quad_numbers(x, y, z)
        renderer.point_numbers(x, y, z)

    image_buffer = renderer.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"debug_renderer_lines{suffix}.png", f"{line_type}")


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("renderer_type", ["mpl", "bokeh"])
def test_renderer_filled(show_text: bool, fill_type: FillType, renderer_type: str) -> None:
    if renderer_type == "bokeh":
        try:
            from contourpy.util.bokeh_renderer import BokehRenderer as Renderer
        except ImportError:
            pytest.skip("Optional bokeh dependencies not installed")
    elif renderer_type == "mpl":
        from contourpy.util.mpl_renderer import MplRenderer as Renderer  # type: ignore
    else:
        raise ValueError(f"Unrecognised renderer type {renderer_type}")

    from .image_comparison import compare_images

    x, y, z = random((3, 4), mask_fraction=0.35)
    renderer = Renderer(ncols=2, figsize=(8, 3), show_frame=False)
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
            renderer.mask(x, y, z, ax=ax, color="red")
            if show_text:
                renderer.title("Title", ax=ax)
        else:
            renderer.grid(x, y, ax=ax, alpha=0.8, point_color="black")
            if show_text:
                renderer.title("Colored title", ax=ax, color="red")

    image_buffer = renderer.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(
        image_buffer, f"renderer_filled_{renderer_type}{suffix}.png", f"{fill_type}",
        mean_threshold=0.03 if renderer_type == "bokeh" else None,
    )


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("renderer_type", ["mpl", "bokeh"])
def test_renderer_lines(show_text: bool, line_type: LineType, renderer_type: str) -> None:
    if renderer_type == "bokeh":
        try:
            from contourpy.util.bokeh_renderer import BokehRenderer as Renderer
        except ImportError:
            pytest.skip("Optional bokeh dependencies not installed")
    elif renderer_type == "mpl":
        from contourpy.util.mpl_renderer import MplRenderer as Renderer  # type: ignore
    else:
        raise ValueError(f"Unrecognised renderer type {renderer_type}")

    from .image_comparison import compare_images

    x, y, z = random((3, 4), mask_fraction=0.35)
    renderer = Renderer(ncols=2, figsize=(8, 3), show_frame=show_text)
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
    compare_images(
        image_buffer, f"renderer_lines_{renderer_type}{suffix}.png", f"{line_type}",
        mean_threshold=0.03 if renderer_type == "bokeh" else None,
    )
