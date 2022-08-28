from functools import reduce
from operator import add
import platform

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest

from contourpy import FillType, contour_generator
from contourpy.util.data import random, simple

from . import util_test


@pytest.fixture
def two_outers_one_hole():
    x, y = np.meshgrid([0., 1., 2., 3.], [0., 1., 2.])
    z = np.array([[1.5, 1.5, 0.9, 0.0],
                  [1.5, 2.8, 0.4, 0.8],
                  [0.0, 0.0, 0.8, 1.9]])
    return x, y, z


@pytest.fixture
def xyz_chunk_test():
    x, y = np.meshgrid(np.arange(5), np.arange(5))
    z = 0.5*np.abs(y - 2) + 0.1*(x - 2)
    return x, y, z


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_simple(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (1, 1)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_simple.png", f"{name}_{fill_type}")


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_simple_chunk(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type, chunk_size=2)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "filled_simple_chunk.png", f"{name}_{fill_type}", mean_threshold=0.12,
    )


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_filled_simple_chunk_threads(fill_type, thread_count):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(
        x, y, z, name="threaded", fill_type=fill_type, chunk_size=2, thread_count=thread_count,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "filled_simple_chunk.png", f"{fill_type}_{thread_count}", mean_threshold=0.12,
    )


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_simple_no_corner_mask(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type, corner_mask=False)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (1, 1)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_simple_no_corner_mask.png", f"{name}_{fill_type}")


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_simple_no_corner_mask_chunk(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(
        x, y, z, name=name, fill_type=fill_type, corner_mask=False, chunk_size=2,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "filled_simple_no_corner_mask_chunk.png", f"{name}_{fill_type}",
        mean_threshold=0.11,
    )


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_filled_simple_no_corner_mask_chunk_threads(fill_type, thread_count):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(
        x, y, z, name="threaded", fill_type=fill_type, corner_mask=False, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "filled_simple_no_corner_mask_chunk.png", f"{fill_type}_{thread_count}",
        mean_threshold=0.11,
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_filled_simple_corner_mask(name):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    fill_type = FillType.OuterCode
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type, corner_mask=True)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (1, 1)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_simple_corner_mask.png", f"{name}_{fill_type}")


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_filled_simple_corner_mask_chunk(name):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    fill_type = FillType.OuterCode
    cont_gen = contour_generator(
        x, y, z, name=name, fill_type=fill_type, corner_mask=True, chunk_size=2,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "filled_simple_corner_mask_chunk.png", f"{name}_{fill_type}",
        mean_threshold=0.10,
    )


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_filled_simple_corner_mask_chunk_threads(fill_type, thread_count):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    fill_type = FillType.OuterCode
    cont_gen = contour_generator(
        x, y, z, name="threaded", fill_type=fill_type, corner_mask=True, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "filled_simple_corner_mask_chunk.png", f"{fill_type}_{thread_count}",
        mean_threshold=0.10,
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_filled_simple_quad_as_tri(name):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, quad_as_tri=True)
    levels = np.arange(-1.0, 1.01, 0.1)

    fill_type = cont_gen.fill_type
    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_simple_quad_as_tri.png", f"{name}")


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (1, 1)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_random.png", f"{name}_{fill_type}")


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random_chunk(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type, chunk_size=2)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    max_threshold = None
    mean_threshold = None
    if name == "mpl2005":
        max_threshold = 128
        mean_threshold = 0.16
    elif name in ("serial", "threaded"):
        if fill_type in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset):
            max_threshold = 99
            mean_threshold = 0.142
        else:
            max_threshold = 135
            mean_threshold = 0.19

    compare_images(
        image_buffer, "filled_random_chunk.png", f"{name}_{fill_type}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_filled_random_chunk_threads(fill_type, thread_count):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(
        x, y, z, name="threaded", fill_type=fill_type, chunk_size=2, thread_count=thread_count,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    if fill_type in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset):
        max_threshold = 99
        mean_threshold = 0.142
    else:
        max_threshold = 135
        mean_threshold = 0.19

    compare_images(
        image_buffer, "filled_random_chunk.png", f"{fill_type}_{thread_count}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random_no_corner_mask(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (1, 1)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_random_no_corner_mask.png", f"{name}_{fill_type}")


@pytest.mark.image
@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random_no_corner_mask_chunk(name, fill_type):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name=name, fill_type=fill_type, corner_mask=False, chunk_size=2,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    max_threshold = None
    mean_threshold = None
    if name == "mpl2005":
        max_threshold = 128
        mean_threshold = 0.19
    elif name in ("serial", "threaded"):
        if fill_type in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset):
            max_threshold = 99
            mean_threshold = 0.18
        else:
            max_threshold = 135
            mean_threshold = 0.23

    compare_images(
        image_buffer, "filled_random_no_corner_mask_chunk.png", f"{name}_{fill_type}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_filled_random_no_corner_mask_chunk_threads(fill_type, thread_count):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name="threaded", fill_type=fill_type, corner_mask=False, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    if fill_type in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset):
        max_threshold = 99
        mean_threshold = 0.18
    else:
        max_threshold = 135
        mean_threshold = 0.23

    compare_images(
        image_buffer, "filled_random_no_corner_mask_chunk.png", f"{fill_type}_{thread_count}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_filled_random_corner_mask(name):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    fill_type = FillType.OuterCode
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=True, fill_type=fill_type)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (1, 1)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_random_corner_mask.png", f"{name}_{fill_type}")


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_filled_random_corner_mask_chunk(name):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    fill_type = FillType.OuterCode
    cont_gen = contour_generator(
        x, y, z, name=name, corner_mask=True, fill_type=fill_type, chunk_size=2,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    max_threshold = None
    mean_threshold = None
    if name in ("serial", "threaded"):
        max_threshold = 135
        mean_threshold = 0.17

    compare_images(
        image_buffer, "filled_random_corner_mask_chunk.png", f"{name}_{fill_type}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_filled_random_corner_mask_chunk_threads(fill_type, thread_count):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    fill_type = FillType.OuterCode
    cont_gen = contour_generator(
        x, y, z, name="threaded", corner_mask=True, fill_type=fill_type, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "filled_random_corner_mask_chunk.png", f"{fill_type}_{thread_count}",
        max_threshold=135, mean_threshold=0.17,
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_filled_random_quad_as_tri(name):
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, quad_as_tri=True)
    levels = np.arange(0.0, 1.01, 0.2)

    fill_type = cont_gen.fill_type
    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_random_quad_as_tri.png", f"{name}")


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("name", ["serial", "threaded"])
def test_return_by_fill_type(two_outers_one_hole, name, fill_type):
    x, y, z = two_outers_one_hole
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type)
    assert cont_gen.fill_type == fill_type
    filled = cont_gen.filled(1.0, 2.0)

    util_test.assert_filled(filled, fill_type)

    if fill_type in (FillType.OuterCode, FillType.OuterOffset):
        points = filled[0]
        assert len(points) == 2
        assert points[0].shape == (13, 2)
        assert points[1].shape == (4, 2)
        assert_array_equal(points[0][0], points[0][7])
        assert_array_equal(points[0][8], points[0][12])
        assert_array_equal(points[1][0], points[1][3])
        if fill_type == FillType.OuterCode:
            codes = filled[1]
            assert_array_equal(codes[0], [1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79])
            assert_array_equal(codes[1], [1, 2, 2, 79])
        else:
            offsets = filled[1]
            assert_array_equal(offsets[0], [0, 8, 13])
            assert_array_equal(offsets[1], [0, 4])
    else:
        points = filled[0]
        assert len(points) == 1
        points = points[0]
        assert points.shape == (17, 2)
        assert_array_equal(points[0], points[7])
        assert_array_equal(points[8], points[12])
        assert_array_equal(points[13], points[16])
        if fill_type in (FillType.ChunkCombinedCode, FillType.ChunkCombinedCodeOffset):
            codes = filled[1][0]
            assert_array_equal(codes, [1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79, 1, 2, 2, 79])
        else:
            offsets = filled[1][0]
            assert_array_equal(offsets, [0, 8, 13, 17])

        if fill_type == FillType.ChunkCombinedCodeOffset:
            outer_offsets = filled[2][0]
            assert_array_equal(outer_offsets, [0, 13, 17])
        elif fill_type == FillType.ChunkCombinedOffsetOffset:
            outer_offsets = filled[2][0]
            assert_array_equal(outer_offsets, [0, 2, 3])


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("name, thread_count",
                         [("serial", 1), ("threaded", 1), ("threaded", 2)])
def test_return_by_fill_type_chunk(xyz_chunk_test, name, thread_count, fill_type):
    if platform.python_implementation() == "PyPy" and thread_count > 1:
        pytest.skip()

    x, y, z = xyz_chunk_test
    kwargs = dict(name=name, fill_type=fill_type, chunk_count=2)
    if name == "threaded":
        kwargs["thread_count"] = thread_count
    cont_gen = contour_generator(x, y, z, **kwargs)
    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (2, 2)
    assert cont_gen.chunk_size == (2, 2)
    if name == "threaded":
        assert cont_gen.thread_count == thread_count
    filled = cont_gen.filled(0.45, 0.55)

    util_test.assert_filled(filled, fill_type)

    # Expected points by chunk.
    expected = (
        [[0.0, 0.7], [0.0, 0.5], [1.0, 0.7], [2.0, 0.9], [2.0, 1.0], [2.0, 1.1], [1.5, 1.0],
         [1.0, 0.9], [0.0, 0.7]],
        [[2.0, 1.0], [2.0, 0.9], [2.5, 1.0], [3.0, 1.1], [4.0, 1.3], [4.0, 1.5], [3.0, 1.3],
         [2.0, 1.1], [2.0, 1.0]],
        [[1.5, 3.0], [2.0, 2.9], [2.0, 3.0], [2.0, 3.1], [1.0, 3.3], [0.0, 3.5], [0.0, 3.3],
         [1.0, 3.1], [1.5, 3.0]],
        [[2.0, 3.0], [2.0, 2.9], [3.0, 2.7], [4.0, 2.5], [4.0, 2.7], [3.0, 2.9], [2.5, 3.0],
         [2.0, 3.1], [2.0, 3.0]],
    )

    if fill_type in (FillType.OuterCode, FillType.OuterOffset):
        points = filled[0]
        assert len(points) == 4
        if name == "threaded" and cont_gen.thread_count > 1:
            # Polygons may be in any order so sort lines and expected.
            points = sorted([polygon.tolist() for polygon in points])
            expected = sorted(expected)
        for chunk in range(4):
            assert_allclose(points[chunk], expected[chunk])

        if fill_type == FillType.OuterCode:
            codes = filled[1]
            for chunk in range(4):
                assert_array_equal(codes[chunk], [1, 2, 2, 2, 2, 2, 2, 2, 79])
        else:
            offsets = filled[1]
            for chunk in range(4):
                assert_array_equal(offsets[chunk], [0, 9])
    else:
        points = filled[0]
        assert len(points) == 4
        for chunk in range(4):
            assert_allclose(points[chunk], expected[chunk])

        if fill_type in (FillType.ChunkCombinedCode, FillType.ChunkCombinedCodeOffset):
            codes = filled[1]
            for chunk in range(4):
                assert_array_equal(codes[chunk], [1, 2, 2, 2, 2, 2, 2, 2, 79])
        else:
            offsets = filled[1]
            for chunk in range(4):
                assert_array_equal(offsets[chunk], [0, 9])

        if fill_type == FillType.ChunkCombinedCodeOffset:
            outer_offsets = filled[2]
            for chunk in range(4):
                assert_array_equal(outer_offsets[chunk], [0, 9])
        elif fill_type == FillType.ChunkCombinedOffsetOffset:
            outer_offsets = filled[2]
            for chunk in range(4):
                assert_array_equal(outer_offsets[chunk], [0, 1])


@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
@pytest.mark.parametrize("corner_mask", [None, False, True])
def test_filled_random_big(name, fill_type, corner_mask):
    if corner_mask and name in ["mpl2005", "mpl2014"]:
        pytest.skip()

    x, y, z = random((1000, 1000), mask_fraction=0.0 if corner_mask is None else 0.05)
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=corner_mask, fill_type=fill_type)
    levels = np.arange(0.0, 1.01, 0.1)

    assert cont_gen.fill_type == fill_type

    for i in range(len(levels)-1):
        filled = cont_gen.filled(levels[i], levels[i+1])
        util_test.assert_filled(filled, fill_type)


@pytest.mark.slow
@pytest.mark.parametrize('seed', np.arange(10))
def test_filled_compare_slow(seed):
    x, y, z = random((1000, 1000), mask_fraction=0.05, seed=seed)
    levels = np.arange(0.0, 1.01, 0.1)

    cont_gen_mpl2014 = contour_generator(x, y, z, name="mpl2014", corner_mask=True)
    cont_gen_serial = contour_generator(
        x, y, z, name="serial", corner_mask=True, fill_type=FillType.ChunkCombinedOffsetOffset)

    assert cont_gen_mpl2014.fill_type == FillType.OuterCode
    assert cont_gen_serial.fill_type == FillType.ChunkCombinedOffsetOffset

    for i in range(len(levels)-1):
        filled_mpl2014 = cont_gen_mpl2014.filled(levels[i], levels[i+1])
        util_test.assert_filled(filled_mpl2014, cont_gen_mpl2014.fill_type)

        filled_serial = cont_gen_serial.filled(levels[i], levels[i+1])
        util_test.assert_filled(filled_serial, cont_gen_serial.fill_type)

        # Check same results obtained for each in terms of number of points, etc.
        code_list = filled_mpl2014[1]
        n_points = reduce(add, map(len, code_list))
        n_outers = len(code_list)
        n_lines = reduce(add, map(lambda c: np.count_nonzero(c == 1), code_list))

        assert n_points == len(filled_serial[0][0])
        assert n_lines == len(filled_serial[1][0]) - 1
        assert n_outers == len(filled_serial[2][0]) - 1
