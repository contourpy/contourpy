import pytest

from . import util_test


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.all_names())
def test_config_filled(show_text, name):
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigFilled(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_filled{suffix}.png", name)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_config_filled_quad_as_tri(show_text, name):
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigFilled(name, quad_as_tri=True, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_filled_quad_as_tri{suffix}.png", name)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_config_filled_corner(show_text, name):
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigFilledCorner(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_filled_corner{suffix}.png", name)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.all_names())
def test_config_lines(show_text, name):
    from . import util_config
    from .image_comparison import compare_images

    if name == "mpl2005":
        pytest.skip()  # Line directions are not consistent.
    config = util_config.ConfigLines(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_lines{suffix}.png", name)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_config_lines_quad_as_tri(show_text, name):
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigLines(name, quad_as_tri=True, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_lines_quad_as_tri{suffix}.png", name)


@pytest.mark.image
@pytest.mark.text
@pytest.mark.parametrize("show_text", [False, True])
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_config_lines_corner(show_text, name):
    from . import util_config
    from .image_comparison import compare_images

    config = util_config.ConfigLinesCorner(name, show_text=show_text)
    image_buffer = config.save_to_buffer()
    suffix = "" if show_text else "_no_text"
    compare_images(image_buffer, f"config_lines_corner{suffix}.png", name)
