from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Iterator

import numpy as np
import pytest

from contourpy import FillType, LineType, contour_generator
from contourpy.util.data import random

if TYPE_CHECKING:
    from _pytest._py.path import LocalPath
    from _pytest.logging import LogCaptureFixture
    from selenium.webdriver.remote.webdriver import WebDriver

bokeh_renderer = pytest.importorskip("contourpy.util.bokeh_renderer")


@pytest.fixture(scope="session")
def driver(driver_path: str) -> Iterator[WebDriver]:
    # Based on Bokeh's tests/support/plugins/selenium.py
    def chrome() -> WebDriver:
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.webdriver import WebDriver as Chrome

        options = Options()
        options.add_argument("--headless")  # type: ignore[no-untyped-call]
        options.add_argument("--no-sandbox")  # type: ignore[no-untyped-call]

        if driver_path:
            from selenium.webdriver.chrome.service import Service
            service = Service(executable_path=driver_path)
            return Chrome(options=options, service=service)
        else:
            return Chrome(options=options)

    driver = chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_chrome_version(driver: WebDriver) -> None:
    # Print version of chrome used for export to PNG by Bokeh as test images, particularly those
    # containing text, are sensitive to chrome version.
    capabilities = driver.capabilities
    print("Browser used by Bokeh:", capabilities["browserName"], capabilities["browserVersion"])
    if "chrome" in capabilities:
        print("Chromedriver:", capabilities["chrome"]["chromedriverVersion"])


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
def test_renderer_filled_bokeh(show_text: bool, fill_type: FillType, driver: WebDriver) -> None:
    from .image_comparison import compare_images

    renderer = bokeh_renderer.BokehRenderer(ncols=2, figsize=(8, 3), show_frame=False)
    x, y, z = random((3, 4), mask_fraction=0.35)
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

    image_buffer = renderer.save_to_buffer(webdriver=driver)
    suffix = "" if show_text else "_no_text"
    compare_images(
        image_buffer, f"bokeh_renderer_filled{suffix}.png", f"{fill_type}", mean_threshold=0.03,
    )


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("line_type", LineType.__members__.values())
def test_renderer_lines_bokeh(show_text: bool, line_type: LineType, driver: WebDriver) -> None:
    from .image_comparison import compare_images

    renderer = bokeh_renderer.BokehRenderer(ncols=2, figsize=(8, 3), show_frame=show_text)
    x, y, z = random((3, 4), mask_fraction=0.35)
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

    image_buffer = renderer.save_to_buffer(webdriver=driver)
    suffix = "" if show_text else "_no_text"
    compare_images(
        image_buffer, f"bokeh_renderer_lines{suffix}.png", f"{line_type}", mean_threshold=0.03,
    )


@pytest.mark.image
@pytest.mark.parametrize("transparent", [False, True])
def test_save_png(
    transparent: bool, tmpdir: LocalPath, driver: WebDriver, caplog: LogCaptureFixture,
) -> None:
    from PIL import Image

    renderer = bokeh_renderer.BokehRenderer(figsize=(4, 3), show_frame=False)
    filename = (tmpdir / "bokeh.png").strpath

    with caplog.at_level(logging.ERROR):  # Hide Bokeh warnings about no renderers.
        renderer.save(filename, transparent, webdriver=driver)

    # Testing that a PNG file is produced of the correct size and format.
    # Not testing the actual image produced except for the first pixel to confirm transparency.
    with Image.open(filename) as image:
        assert image.format == "PNG"
        assert image.mode == "RGBA"
        assert image.size == (400, 300)
        rgba = image.getpixel((0, 0))

        # Transparent background not working for PNG export.
        # assert rgba[3] == 0 if transparent else 255
        assert rgba[3] == 255


@pytest.mark.image
@pytest.mark.parametrize("transparent", [False, True])
def test_save_svg(
    transparent: bool, tmpdir: LocalPath, driver: WebDriver, caplog: LogCaptureFixture,
) -> None:
    renderer = bokeh_renderer.BokehRenderer(figsize=(4, 3), show_frame=False, want_svg=True)
    filename = (tmpdir / "bokeh.svg").strpath

    with caplog.at_level(logging.ERROR):  # Hide Bokeh warnings about no renderers.
        renderer.save(filename, transparent, webdriver=driver)

    # Rather simplistic check of SVG file contents.
    with open(filename) as f:
        svg = f.read()

    assert svg[:5] == "<svg "
    count0 = len(re.findall('fill-opacity="0"', svg))
    count1 = len(re.findall('fill-opacity="1"', svg))
    if transparent:
        assert count0 == 2 and count1 == 0
    else:
        assert count0 == 2 and count1 == 2
