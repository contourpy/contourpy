from __future__ import annotations

import gc
import platform
from typing import TYPE_CHECKING

import pytest

from . import util_test

if TYPE_CHECKING:
    from .util_config import Config


def cleanup(config: Config) -> None:
    if platform.python_implementation() == "PyPy":
        config.clear()
        gc.collect()


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.all_names())
def test_config_filled(show_text: bool, name: str) -> None:
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigFilled(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_filled{suffix}.png", name)
    cleanup(config)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.flaky(reruns=1, condition=platform.python_implementation().startswith("PyPy"))
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_config_filled_quad_as_tri(show_text: bool, name: str) -> None:
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigFilled(name, quad_as_tri=True, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_filled_quad_as_tri{suffix}.png", name)
    cleanup(config)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_config_filled_corner(show_text: bool, name: str) -> None:
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigFilledCorner(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_filled_corner{suffix}.png", name)
    cleanup(config)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.all_names())
def test_config_lines(show_text: bool, name: str) -> None:
    from . import util_config
    from .image_comparison import compare_images

    if name == "mpl2005":
        pytest.skip()  # Line directions are not consistent.
    config = util_config.ConfigLines(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_lines{suffix}.png", name)
    cleanup(config)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_config_lines_quad_as_tri(show_text: bool, name: str) -> None:
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigLines(name, quad_as_tri=True, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_lines_quad_as_tri{suffix}.png", name)
    cleanup(config)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_config_lines_corner(show_text: bool, name: str) -> None:
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigLinesCorner(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_lines_corner{suffix}.png", name)
    cleanup(config)
