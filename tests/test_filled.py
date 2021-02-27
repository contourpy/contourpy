import contourpy
from image_comparison import compare_images
import numpy as np
import pytest
import util_data
import util_renderer
import util_test


@pytest.mark.parametrize('name', util_test.all_names())
def test_filled_random_uniform_no_corner_mask(name):
    x, y, z = util_data.random_uniform((30, 40), mask_fraction=0.05)
    cont_gen = contourpy.contour_generator(x, y, z, name=name, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = util_renderer.Renderer(x, y)
    for i in range(len(levels)-1):
        renderer.add_filled(cont_gen.contour_filled(levels[i], levels[i+1]),
                            color=f'C{i}')
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, 'filled_random_uniform_no_corner_mask.png',
                   name, max_threshold=150 if name == 'mpl2005' else 10)


@pytest.mark.parametrize('name', util_test.corner_mask_names())
def test_filled_random_uniform_corner_mask(name):
    x, y, z = util_data.random_uniform((30, 40), mask_fraction=0.05)
    cont_gen = contourpy.contour_generator(x, y, z, name=name, corner_mask=True)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = util_renderer.Renderer(x, y)
    for i in range(len(levels)-1):
        renderer.add_filled(cont_gen.contour_filled(levels[i], levels[i+1]),
                            color=f'C{i}')
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, 'filled_random_uniform_corner_mask.png', name)
