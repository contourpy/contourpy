import contourpy
from image_comparison import compare_images
import numpy as np
from numpy.testing import assert_allclose
import pytest
import util_data
import util_renderer


@pytest.fixture
def xy_2x2():
    return np.meshgrid([0.0, 1.0], [0.0, 1.0])


@pytest.fixture
def xy_3x3():
    return np.meshgrid([0.0, 0.5, 1.0], [0.0, 0.5, 1.0])


@pytest.mark.parametrize('zlevel', (-1e-10, 1.0+1e10, np.nan, -np.nan, np.inf, -np.inf))
def test_level_outside(xy_2x2, zlevel):
    x, y = xy_2x2
    z = x
    cont_gen = contourpy.contour_generator(x, y, z)
    lines = cont_gen.contour_lines(zlevel)
    assert(isinstance(lines, list))
    assert(len(lines) == 0)


def test_w_to_e(xy_2x2):
    x, y = xy_2x2
    z = y.copy()
    cont_gen = contourpy.contour_generator(x, y, z)
    lines = cont_gen.contour_lines(0.5)
    assert(len(lines) == 1)
    line = lines[0]
    np.testing.assert_allclose(line, [[0.0, 0.5], [1.0, 0.5]])


def test_e_to_w(xy_2x2):
    x, y = xy_2x2
    z = 1.0 - y.copy()
    cont_gen = contourpy.contour_generator(x, y, z)
    lines = cont_gen.contour_lines(0.5)
    assert(len(lines) == 1)
    line = lines[0]
    assert_allclose(line, [[1.0, 0.5], [0.0, 0.5]])


def test_loop(xy_3x3):
    x, y = xy_3x3
    z = np.zeros_like(x)
    z[1, 1] = 1.0
    cont_gen = contourpy.contour_generator(x, y, z)
    lines = cont_gen.contour_lines(0.5)
    assert(len(lines) == 1)
    line = lines[0]
    assert(line.shape == (5, 2))
    assert_allclose(line[0], line[-1])


def test_lines_random_uniform_no_corner_mask():
    x, y, z = util_data.random_uniform((30, 40), mask_fraction=0.05)
    cont_gen = contourpy.contour_generator(x, y, z, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = util_renderer.Renderer(x, y)
    for i in range(len(levels)):
        renderer.add_lines(cont_gen.contour_lines(levels[i]), color=f'C{i}')
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer,
                   'lines_random_uniform_no_corner_mask.png')
