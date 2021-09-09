from image_comparison import compare_images
import pytest
import util_config
import util_test


@pytest.mark.parametrize("name", util_test.all_names())
def test_config_filled(name):
    config = util_config.ConfigFilled(name)
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, "config_filled.png", name)


@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_config_filled_quad_as_tri(name):
    config = util_config.ConfigFilled(name, quad_as_tri=True)
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, "config_filled_quad_as_tri.png", name)


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_config_filled_corner(name):
    config = util_config.ConfigFilledCorner(name)
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, "config_filled_corner.png", name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_config_lines(name):
    if name == "mpl2005":
        pytest.skip()  # Line directions are not consistent.
    config = util_config.ConfigLines(name)
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, "config_lines.png", name)


@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_config_lines_quad_as_tri(name):
    config = util_config.ConfigLines(name, quad_as_tri=True)
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, "config_lines_quad_as_tri.png", name)


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_config_lines_corner(name):
    config = util_config.ConfigLinesCorner(name)
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, "config_lines_corner.png", name)
