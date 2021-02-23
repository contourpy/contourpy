import contourpy
from image_comparison import compare_images
import pytest
import util_config



def test_config_filled():
    config = util_config.ConfigFilled()
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, 'config_filled.png')


def test_config_filled_corner():
    config = util_config.ConfigFilledCorner()
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, 'config_filled_corner.png')


def test_config_lines():
    config = util_config.ConfigLines()
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, 'config_lines.png')


def test_config_lines_corner():
    config = util_config.ConfigLinesCorner()
    image_buffer = config.save_to_buffer()
    compare_images(image_buffer, 'config_lines_corner.png')
