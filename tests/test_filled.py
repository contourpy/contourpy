from contourpy import contour_generator, FillType
from contourpy.util.data import random
from contourpy.util.mpl_renderer import MplTestRenderer
from image_comparison import compare_images
import numpy as np
from numpy.testing import assert_array_equal
import pytest
import util_test


@pytest.fixture
def two_outers_one_hole():
    x, y = np.meshgrid([0., 1., 2., 3.], [0., 1., 2.])
    z = np.array([[1.5, 1.5, 0.9, 0.0],
                  [1.5, 2.8, 0.4, 0.8],
                  [0.0, 0.0, 0.8, 1.9]])
    return x, y, z


@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random(name, fill_type):
    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_random.png", f"{name}_{fill_type}")


@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random_chunk(name, fill_type):
    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type, chunk_size=2)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type

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
        if fill_type in (FillType.ChunkCombinedCodes, FillType.ChunkCombinedOffsets):
            max_threshold = 99
            mean_threshold = 0.14
        else:
            max_threshold = 134
            mean_threshold = 0.19

    compare_images(
        image_buffer, "filled_random_chunk.png", f"{name}_{fill_type}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
        )


@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random_no_corner_mask(name, fill_type):
    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(x, y, z, name=name, fill_type=fill_type, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.fill_type == fill_type

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_random_no_corner_mask.png", f"{name}_{fill_type}")


@pytest.mark.parametrize("name, fill_type", util_test.all_names_and_fill_types())
def test_filled_random_no_corner_mask_chunk(name, fill_type):
    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name=name, fill_type=fill_type, corner_mask=False, chunk_size=2)
    levels = np.arange(0.0, 1.01, 0.2)

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
        if fill_type in (FillType.ChunkCombinedCodes, FillType.ChunkCombinedOffsets):
            max_threshold = 99
            mean_threshold = 0.18
        else:
            max_threshold = 135
            mean_threshold = 0.23

    compare_images(
        image_buffer, "filled_random_no_corner_mask_chunk.png", f"{name}_{fill_type}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_filled_random_corner_mask(name):
    x, y, z = random((30, 40), mask_fraction=0.05)
    fill_type = FillType.OuterCodes
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=True, fill_type=fill_type)
    levels = np.arange(0.0, 1.01, 0.2)

    renderer = MplTestRenderer()
    for i in range(len(levels)-1):
        renderer.filled(cont_gen.filled(levels[i], levels[i+1]), fill_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "filled_random_corner_mask.png", f"{name}_{fill_type}")


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_filled_random_corner_mask_chunk(name):
    x, y, z = random((30, 40), mask_fraction=0.05)
    fill_type = FillType.OuterCodes
    cont_gen = contour_generator(
        x, y, z, name=name, corner_mask=True, fill_type=fill_type, chunk_size=2)
    levels = np.arange(0.0, 1.01, 0.2)

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


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("name", ["serial"])
def test_return_by_fill_type(two_outers_one_hole, name, fill_type):
    x, y, z = two_outers_one_hole
    cont_gen = contour_generator(x, y, z, name, fill_type=fill_type)
    assert cont_gen.fill_type == fill_type
    filled = cont_gen.filled(1.0, 2.0)
    if fill_type in (FillType.OuterCodes, FillType.OuterOffsets):
        assert isinstance(filled, tuple) and len(filled) == 2
        points = filled[0]
        assert isinstance(points, list) and len(points) == 2
        for p in points:
            assert isinstance(p, np.ndarray)
            assert p.dtype == util_test.point_dtype
        assert points[0].shape == (13, 2)
        assert points[1].shape == (4, 2)
        assert_array_equal(points[0][0], points[0][7])
        assert_array_equal(points[0][8], points[0][12])
        assert_array_equal(points[1][0], points[1][3])
        if fill_type == FillType.OuterCodes:
            codes = filled[1]
            assert isinstance(codes, list) and len(codes) == 2
            for c in codes:
                assert isinstance(c, np.ndarray)
                assert c.dtype == util_test.code_dtype
            assert_array_equal(codes[0], [1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79])
            assert_array_equal(codes[1], [1, 2, 2, 79])
        else:  # FillType.OuterOffsets.
            offsets = filled[1]
            assert isinstance(offsets, list) and len(offsets) == 2
            for o in offsets:
                assert isinstance(o, np.ndarray)
                assert o.dtype == util_test.offset_dtype
            assert_array_equal(offsets[0], [0, 8, 13])
            assert_array_equal(offsets[1], [0, 4])
    elif fill_type in (FillType.ChunkCombinedCodes, FillType.ChunkCombinedOffsets,
                       FillType.ChunkCombinedCodesOffsets, FillType.ChunkCombinedOffsets2):
        if fill_type in (FillType.ChunkCombinedCodes, FillType.ChunkCombinedOffsets):
            assert isinstance(filled, tuple) and len(filled) == 2
        else:
            assert isinstance(filled, tuple) and len(filled) == 3
        points = filled[0]
        assert isinstance(points, list) and len(points) == 1
        points = points[0]
        assert isinstance(points, np.ndarray)
        assert points.dtype == util_test.point_dtype
        assert points.shape == (17, 2)
        assert_array_equal(points[0], points[7])
        assert_array_equal(points[8], points[12])
        assert_array_equal(points[13], points[16])
        if fill_type in (FillType.ChunkCombinedCodes, FillType.ChunkCombinedCodesOffsets):
            codes = filled[1]
            assert isinstance(codes, list) and len(codes) == 1
            codes = codes[0]
            assert isinstance(codes, np.ndarray)
            assert codes.dtype == util_test.code_dtype
            assert_array_equal(codes, [1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79, 1, 2, 2, 79])
        else:
            offsets = filled[1]
            assert isinstance(offsets, list) and len(offsets) == 1
            offsets = offsets[0]
            assert isinstance(offsets, np.ndarray)
            assert offsets.dtype == util_test.offset_dtype
            assert_array_equal(offsets, [0, 8, 13, 17])

        if fill_type in (FillType.ChunkCombinedCodesOffsets, FillType.ChunkCombinedOffsets2):
            outer_offsets = filled[2]
            assert isinstance(outer_offsets, list) and len(outer_offsets) == 1
            outer_offsets = outer_offsets[0]
            assert isinstance(outer_offsets, np.ndarray)
            assert outer_offsets.dtype == util_test.offset_dtype
            if fill_type == FillType.ChunkCombinedCodesOffsets:
                assert_array_equal(outer_offsets, [0, 13, 17])
            else:
                assert_array_equal(outer_offsets, [0, 2, 3])
    else:
        raise RuntimeError(f"Unexpected fill_type {fill_type}")
