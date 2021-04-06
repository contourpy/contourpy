from contourpy import contour_generator, LineType
from contourpy.util import random_uniform, MplTestRenderer
from image_comparison import compare_images
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest
import util_test


@pytest.fixture
def xy_2x2():
    return np.meshgrid([0.0, 1.0], [0.0, 1.0])


@pytest.fixture
def xy_3x3():
    return np.meshgrid([0.0, 0.5, 1.0], [0.0, 0.5, 1.0])


@pytest.fixture
def one_loop_one_strip():
    x, y = np.meshgrid([0., 1., 2., 3.], [0., 1., 2.])
    z = np.array([[1.5, 1.5, 0.9, 0.0],
                  [1.5, 2.8, 0.4, 0.8],
                  [0.0, 0.0, 0.8, 6.0]])
    return x, y, z


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('zlevel', [-1e-10, 1.0+1e10, np.nan, -np.nan, np.inf, -np.inf])
def test_level_outside(xy_2x2, name, zlevel):
    x, y = xy_2x2
    z = x
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=LineType.Separate)
    lines = cont_gen.contour_lines(zlevel)
    assert(isinstance(lines, list))
    assert(len(lines) == 0)


@pytest.mark.parametrize('name', util_test.all_names())
def test_w_to_e(xy_2x2, name):
    x, y = xy_2x2
    z = y.copy()
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=LineType.Separate)
    lines = cont_gen.contour_lines(0.5)
    assert(isinstance(lines, list))
    assert(len(lines) == 1)
    line = lines[0]
    assert_allclose(line, [[0.0, 0.5], [1.0, 0.5]])


@pytest.mark.parametrize('name', util_test.all_names())
def test_e_to_w(xy_2x2, name):
    x, y = xy_2x2
    z = 1.0 - y.copy()
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=LineType.Separate)
    lines = cont_gen.contour_lines(0.5)
    assert(isinstance(lines, list))
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
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=LineType.Separate)
    lines = cont_gen.contour_lines(0.5)
    assert(isinstance(lines, list))
    assert(len(lines) == 1)
    line = lines[0]
    assert(line.shape == (5, 2))
    assert_allclose(line[0], line[-1])


@pytest.mark.parametrize(
    'name, line_type', util_test.all_names_and_line_types())
def test_lines_random_uniform_no_corner_mask(name, line_type):
    x, y, z = random_uniform((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    if name != 'mpl2005':
        assert cont_gen.line_type == line_type

    renderer = MplTestRenderer(x, y)
    for i in range(len(levels)):
        renderer.lines(cont_gen.contour_lines(levels[i]),
                       line_type, color=f'C{i}')
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, 'lines_random_uniform_no_corner_mask.png',
                   f'{name}_{line_type}',
                   max_threshold=200 if name == 'mpl2005' else 100)


@pytest.mark.parametrize(
    'name, line_type', util_test.all_names_and_line_types())
def test_lines_random_uniform_no_corner_mask_chunk(name, line_type):
    if name in ('mpl2005', 'mpl2014'):
        pytest.skip()

    x, y, z = random_uniform((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=False,
        chunk_size=2)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = MplTestRenderer(x, y)
    for i in range(len(levels)):
        renderer.lines(cont_gen.contour_lines(levels[i]),
                       line_type, color=f'C{i}')
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer,
                   'lines_random_uniform_no_corner_mask_chunk.png',
                   f'{name}_{line_type}',
                   max_threshold=200 if name == 'mpl2005' else 100)


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

    compare_images(image_buffer, 'lines_random_uniform_corner_mask.png',
                   f'{name}_{line_type}')


@pytest.mark.parametrize('line_type', LineType.__members__.values())
@pytest.mark.parametrize('name', ['serial'])
def test_return_by_line_type(one_loop_one_strip, name, line_type):
    x, y, z = one_loop_one_strip
    cont_gen = contour_generator(x, y, z, name, line_type=line_type)
    assert cont_gen.line_type == line_type
    lines = cont_gen.contour_lines(2.0)
    if line_type in (LineType.Separate, LineType.SeparateCodes):
        if line_type == LineType.SeparateCodes:
            assert isinstance(lines, tuple) and len(lines) == 2
            points = lines[0]
        else:
            points = lines
        assert isinstance(points, list) and len(points) == 2
        for p in points:
            assert isinstance(p, np.ndarray)
            assert p.dtype == np.float64
        assert points[0].shape == (5, 2)
        assert points[1].shape == (2, 2)
        assert_array_equal(points[0][0], points[0][4])
        if line_type == LineType.SeparateCodes:
            codes = lines[1]
            assert isinstance(codes, list) and len(codes) == 2
            for c in codes:
                assert isinstance(c, np.ndarray)
                assert c.dtype == np.uint8
            assert_array_equal(codes[0], [1, 2, 2, 2, 79])
            assert_array_equal(codes[1], [1, 2])
    elif line_type in (LineType.ChunkCombinedCodes,
                       LineType.ChunkCombinedOffsets):
        assert isinstance(lines, tuple) and len(lines) == 2
        points = lines[0]
        assert isinstance(points, list) and len(points) == 1
        assert isinstance(points[0], np.ndarray)
        assert points[0].dtype == np.float64
        assert points[0].shape == (7, 2)
        assert_array_equal(points[0][0], points[0][4])
        if line_type == LineType.ChunkCombinedCodes:
            codes = lines[1]
            assert isinstance(codes, list) and len(codes) == 1
            assert isinstance(codes[0], np.ndarray)
            assert codes[0].dtype == np.uint8
            assert_array_equal(codes[0], [1, 2, 2, 2, 79, 1, 2])
        else:
            offsets = lines[1]
            assert isinstance(offsets, list) and len(offsets) == 1
            assert isinstance(offsets[0], np.ndarray)
            assert offsets[0].dtype == np.int32
            assert_array_equal(offsets[0], [0, 5, 7])
    else:
        raise RuntimeError(f'Unexpected line_type {line_type}')
