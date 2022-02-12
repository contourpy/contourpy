import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest

from contourpy import contour_generator, LineType
from contourpy.util.data import random, simple
from contourpy.util.mpl_renderer import MplTestRenderer
from image_comparison import compare_images
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


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("zlevel", [-1e-10, 1.0+1e10, np.nan, -np.nan, np.inf, -np.inf])
def test_level_outside(xy_2x2, name, zlevel):
    x, y = xy_2x2
    z = x
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(zlevel)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 0
    assert isinstance(codes, list) and len(codes) == 0


@pytest.mark.parametrize("name", util_test.all_names())
def test_w_to_e(xy_2x2, name):
    x, y = xy_2x2
    z = y.copy()
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(0.5)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 1
    assert isinstance(codes, list) and len(codes) == 1
    assert_allclose(points[0], [[0.0, 0.5], [1.0, 0.5]])
    assert_array_equal(codes[0], [1, 2])


@pytest.mark.parametrize("name", util_test.all_names())
def test_e_to_w(xy_2x2, name):
    x, y = xy_2x2
    z = 1.0 - y.copy()
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(0.5)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 1
    assert isinstance(codes, list) and len(codes) == 1
    if name == "mpl2005":    # Line directions are not consistent.
        assert_allclose(points[0], [[0.0, 0.5], [1.0, 0.5]])
    else:
        assert_allclose(points[0], [[1.0, 0.5], [0.0, 0.5]])
    assert_array_equal(codes[0], [1, 2])


@pytest.mark.parametrize("name", util_test.all_names())
def test_loop(xy_3x3, name):
    x, y = xy_3x3
    z = np.zeros_like(x)
    z[1, 1] = 1.0
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(0.5)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 1
    assert isinstance(codes, list) and len(codes) == 1
    line = points[0]
    assert line.shape == (5, 2)
    assert_allclose(line[0], line[-1])
    assert_array_equal(codes[0], [1, 2, 2, 2, 79])


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple(name, line_type):
    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple_chunk(name, line_type):
    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, chunk_size=2)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_chunk.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple_no_corner_mask(name, line_type):
    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, corner_mask=False)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_no_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple_no_corner_mask_chunk(name, line_type):
    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=False, chunk_size=2)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_no_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_simple_corner_mask(name):
    x, y, z = simple((30, 40), want_mask=True)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, corner_mask=True)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_simple_corner_mask_chunk(name):
    x, y, z = simple((30, 40), want_mask=True)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=True, chunk_size=2)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_lines_simple_quad_as_tri(name):
    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, quad_as_tri=True)
    levels = np.arange(-1.0, 1.01, 0.1)

    line_type = cont_gen.line_type
    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_quad_as_tri.png", f"{name}")


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random(name, line_type):
    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random.png", f"{name}_{line_type}", max_threshold=103)


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random_chunk(name, line_type):
    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, chunk_size=2)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    max_threshold = None
    mean_threshold = None
    if name == 'mpl2005':
        max_threshold = 126
        mean_threshold = 0.11

    compare_images(
        image_buffer, "lines_random_chunk.png", f"{name}_{line_type}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random_no_corner_mask(name, line_type):
    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_no_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random_no_corner_mask_chunk(name, line_type):
    if name in ("mpl2005"):
        pytest.skip()  # mpl2005 does not support chunks for lines.

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=False, chunk_size=2)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_no_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_random_corner_mask(name):
    x, y, z = random((30, 40), mask_fraction=0.05)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=True, line_type=line_type)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_random_corner_mask_chunk(name):
    x, y, z = random((30, 40), mask_fraction=0.05)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=True, line_type=line_type)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_lines_random_quad_as_tri(name):
    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, quad_as_tri=True)
    levels = np.arange(0.0, 1.01, 0.2)

    line_type = cont_gen.line_type
    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_quad_as_tri.png", f"{name}")


@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("name", ["serial"])
def test_return_by_line_type(one_loop_one_strip, name, line_type):
    x, y, z = one_loop_one_strip
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type)
    assert cont_gen.line_type == line_type
    lines = cont_gen.lines(2.0)

    util_test.assert_lines(lines, line_type)

    if line_type == LineType.Separate:
        points = lines
        assert len(points) == 2
        assert points[0].shape == (5, 2)
        assert points[1].shape == (2, 2)
    elif line_type == LineType.SeparateCode:
        points, codes = lines
        assert len(points) == 2
        assert points[0].shape == (5, 2)
        assert points[1].shape == (2, 2)
        assert_array_equal(codes[0], [1, 2, 2, 2, 79])
        assert_array_equal(codes[1], [1, 2])
    elif line_type == LineType.ChunkCombinedCode:
        assert len(lines[0]) == 1  # Single chunk.
        points, codes = lines[0][0], lines[1][0]
        assert points.shape == (7, 2)
        assert_array_equal(codes, [1, 2, 2, 2, 79, 1, 2])
    elif line_type == LineType.ChunkCombinedOffset:
        assert len(lines[0]) == 1  # Single chunk.
        points, offsets = lines[0][0], lines[1][0]
        assert points.shape == (7, 2)
        assert_array_equal(offsets, [0, 5, 7])


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
@pytest.mark.parametrize("corner_mask", [None, False, True])
def test_lines_random_big(name, line_type, corner_mask):
    if corner_mask and name in ["mpl2005", "mpl2014"]:
        pytest.skip()

    x, y, z = random((1000, 1000), mask_fraction=0.0 if corner_mask is None else 0.05)
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=corner_mask, line_type=line_type)
    levels = np.arange(0.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type

    for level in levels:
        lines = cont_gen.lines(level)
        util_test.assert_lines(lines, line_type)
