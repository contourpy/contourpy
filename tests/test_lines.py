from contourpy import contour_generator, LineType
from contourpy.util import random_uniform, MplTestRenderer
from image_comparison import compare_images
import numpy as np
from numpy.testing import assert_allclose
import pytest
import util_test


@pytest.fixture
def xy_2x2():
    return np.meshgrid([0.0, 1.0], [0.0, 1.0])


@pytest.fixture
def xy_3x3():
    return np.meshgrid([0.0, 0.5, 1.0], [0.0, 0.5, 1.0])


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('zlevel', [-1e-10, 1.0+1e10, np.nan, -np.nan, np.inf, -np.inf])
def test_level_outside(xy_2x2, name, zlevel):
    x, y = xy_2x2
    z = x
    cont_gen = contour_generator(x, y, z, name=name)
    lines = cont_gen.contour_lines(zlevel)
    assert(isinstance(lines, list))
    assert(len(lines) == 0)


@pytest.mark.parametrize('name', util_test.all_names())
def test_w_to_e(xy_2x2, name):
    x, y = xy_2x2
    z = y.copy()
    cont_gen = contour_generator(x, y, z, name=name)
    lines = cont_gen.contour_lines(0.5)
    assert(len(lines) == 1)
    line = lines[0]
    assert_allclose(line, [[0.0, 0.5], [1.0, 0.5]])


@pytest.mark.parametrize('name', util_test.all_names())
def test_e_to_w(xy_2x2, name):
    x, y = xy_2x2
    z = 1.0 - y.copy()
    cont_gen = contour_generator(x, y, z, name=name)
    lines = cont_gen.contour_lines(0.5)
    assert(len(lines) == 1)
    line = lines[0]
    if name == 'mpl2005':    # Line directions are not consistent.
        assert_allclose(line, [[0.0, 0.5], [1.0, 0.5]])
    else:
        assert_allclose(line, [[1.0, 0.5], [0.0, 0.5]])


@pytest.mark.parametrize('name', util_test.all_names())
def test_loop(xy_3x3, name):
    x, y = xy_3x3
    z = np.zeros_like(x)
    z[1, 1] = 1.0
    cont_gen = contour_generator(x, y, z, name=name)
    lines = cont_gen.contour_lines(0.5)
    assert(len(lines) == 1)
    line = lines[0]
    assert(line.shape == (5, 2))
    assert_allclose(line[0], line[-1])


@pytest.mark.parametrize('name', util_test.all_names())
def test_lines_random_uniform_no_corner_mask(name):
    x, y, z = random_uniform((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    line_type = \
        cont_gen.line_type if name != 'mpl2005' else LineType.Separate

    renderer = MplTestRenderer(x, y)
    for i in range(len(levels)):
        renderer.lines(cont_gen.contour_lines(levels[i]),
                       line_type, color=f'C{i}')
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, 'lines_random_uniform_no_corner_mask.png',
                   name, max_threshold=200 if name == 'mpl2005' else 100)


@pytest.mark.parametrize('name', util_test.corner_mask_names())
def test_lines_random_uniform_corner_mask(name):
    x, y, z = random_uniform((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=True)
    levels = np.arange(0.0, 1.01, 0.2)

    line_type = \
        cont_gen.line_type if name != 'mpl2005' else LineType.Separate

    renderer = MplTestRenderer(x, y)
    for i in range(len(levels)):
        renderer.lines(cont_gen.contour_lines(levels[i]),
                       line_type, color=f'C{i}')
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, 'lines_random_uniform_corner_mask.png', name)
