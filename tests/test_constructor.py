from __future__ import annotations

import math
from typing import TYPE_CHECKING

import numpy as np
import pytest

from contourpy import ContourGenerator, FillType, LineType, ZInterp, contour_generator, max_threads

from . import util_test

if TYPE_CHECKING:
    from numpy.typing import ArrayLike

    from contourpy._contourpy import CoordinateArray


@pytest.fixture
def xyz_3x3_as_lists() -> tuple[list[list[int]], ...]:
    x = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    y = [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
    z = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return x, y, z


@pytest.fixture
def xyz_2x3_as_lists() -> tuple[list[list[int]], ...]:  # shape (2, 3)
    x = [[0, 1, 2], [0, 1, 2]]
    y = [[0, 0, 0], [1, 1, 1]]
    z = [[0, 1, 2], [3, 4, 5]]
    return x, y, z


@pytest.fixture
def xyz_7x5_as_arrays() -> tuple[CoordinateArray, ...]:  # shape (7, 5)
    x, y = np.meshgrid([0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5, 6])
    z = x + y
    return x, y, z


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("z", ([1], [[[1]]]))
def test_ndim_z(
    xyz_3x3_as_lists: tuple[list[list[int]], ...],
    name: str,
    z: ArrayLike,
) -> None:
    x, y, _ = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        contour_generator(x, y, z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("all_xyz", ([[1]], [[1], [2]], [[1, 2]]))
def test_z_shape_too_small(all_xyz: ArrayLike, name: str) -> None:
    with pytest.raises(TypeError):
        contour_generator(z=all_xyz, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("wrong_ndim", (None, [1], [[[1]]]))
def test_diff_ndim_xy(
    xyz_3x3_as_lists: tuple[list[list[int]], ...],
    name: str,
    wrong_ndim: ArrayLike,
) -> None:
    x, y, z = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        contour_generator(wrong_ndim, y, z, name=name)
    with pytest.raises(TypeError):
        contour_generator(x, wrong_ndim, z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_xy_None(xyz_3x3_as_lists: tuple[list[list[int]], ...], name: str) -> None:
    _, _, z = xyz_3x3_as_lists
    contour_generator(None, None, z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_xy_not_specified(xyz_3x3_as_lists: tuple[list[list[int]], ...], name: str) -> None:
    _, _, z = xyz_3x3_as_lists
    contour_generator(z=z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_xy_1d(name: str) -> None:
    z = [[0, 1, 2], [3, 4, 5]]
    contour_generator([0, 1, 2], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        contour_generator([0, 1], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        contour_generator([0, 1, 2, 3], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        contour_generator([0, 1, 2], [0], z, name=name)
    with pytest.raises(TypeError):
        contour_generator([0, 1, 2], [0, 1, 2], z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_xy_ndim_more_than_2(name: str) -> None:
    z = [[0, 1, 2], [3, 4, 5]]
    msg = "Inputs x and y must be None, 1D or 2D, not 3D"
    with pytest.raises(TypeError, match=msg):
        contour_generator([[[1]]], [[[2]]], z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("diff_shape", ([[1, 2, 3, 4], [5, 6, 7, 8]], [[1, 2], [3, 4], [5, 6]]))
def test_xyz_diff_shapes(
    xyz_3x3_as_lists: tuple[list[list[int]], ...],
    name: str,
    diff_shape: ArrayLike,
) -> None:
    x, y, z = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        contour_generator(diff_shape, y, z, name=name)
    with pytest.raises(TypeError):
        contour_generator(x, diff_shape, z, name=name)
    with pytest.raises(TypeError):
        contour_generator(x, y, diff_shape, name=name)


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_corner_mask(xyz_3x3_as_lists: tuple[list[list[int]], ...], name: str) -> None:
    x, y, z = xyz_3x3_as_lists
    for corner_mask in [False, True]:
        cont_gen = contour_generator(x, y, z, name=name, corner_mask=corner_mask)
        assert cont_gen.corner_mask == corner_mask


def test_corner_mask_not_supported(xyz_3x3_as_lists: tuple[list[list[int]], ...]) -> None:
    name = "mpl2005"
    x, y, z = xyz_3x3_as_lists
    msg = f"{name} contour generator does not support corner_mask=True"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, corner_mask=True)


@pytest.mark.parametrize("name", util_test.all_names())
def test_chunk_size_negative(xyz_3x3_as_lists: tuple[list[list[int]], ...], name: str) -> None:
    x, y, z = xyz_3x3_as_lists
    msg = "chunk_size cannot be negative"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, chunk_size=-1)
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, chunk_size=(-1, 0))
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, chunk_size=(0, -1))


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("chunk_size", np.arange(9))
def test_chunk_size_1d(
    xyz_7x5_as_arrays: tuple[CoordinateArray, ...],
    name: str,
    chunk_size: int,
) -> None:
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contour_generator(x, y, z, name=name, chunk_size=chunk_size)
    ret_y_chunk_size, ret_x_chunk_size = cont_gen.chunk_size
    ret_y_chunk_count, ret_x_chunk_count = cont_gen.chunk_count
    if chunk_size == 0:
        assert ret_x_chunk_size == nx-1
        assert ret_y_chunk_size == ny-1
    else:
        assert ret_x_chunk_size == min(chunk_size, nx-1)
        assert ret_y_chunk_size == min(chunk_size, ny-1)
    assert ret_y_chunk_count*ret_y_chunk_size >= ny-1
    assert (ret_y_chunk_count-1)*ret_y_chunk_size < ny-1
    assert ret_x_chunk_count*ret_x_chunk_size >= nx-1
    assert (ret_x_chunk_count-1)*ret_x_chunk_size < nx-1


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("x_chunk_size", np.arange(9))
@pytest.mark.parametrize("y_chunk_size", np.arange(9))
def test_chunk_size_2d(
    xyz_7x5_as_arrays: tuple[CoordinateArray, ...],
    name: str,
    x_chunk_size: int,
    y_chunk_size: int,
) -> None:
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contour_generator(x, y, z, name=name, chunk_size=(y_chunk_size, x_chunk_size))
    ret_y_chunk_size, ret_x_chunk_size = cont_gen.chunk_size
    ret_y_chunk_count, ret_x_chunk_count = cont_gen.chunk_count
    if x_chunk_size == 0:
        assert ret_x_chunk_size == nx-1
    else:
        assert ret_x_chunk_size == min(x_chunk_size, nx-1)
    if y_chunk_size == 0:
        assert ret_y_chunk_size == ny-1
    else:
        assert ret_y_chunk_size == min(y_chunk_size, ny-1)
    assert ret_y_chunk_count*ret_y_chunk_size >= ny-1
    assert (ret_y_chunk_count-1)*ret_y_chunk_size < ny-1
    assert ret_x_chunk_count*ret_x_chunk_size >= nx-1
    assert (ret_x_chunk_count-1)*ret_x_chunk_size < nx-1


def test_chunk_size_and_count(xyz_7x5_as_arrays: tuple[CoordinateArray, ...]) -> None:
    x, y, z = xyz_7x5_as_arrays
    name = "serial"
    msg = "Only one of chunk_size, chunk_count and total_chunk_count should be set"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, chunk_size=1, chunk_count=1)
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, chunk_size=1, total_chunk_count=1)
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, chunk_count=1, total_chunk_count=1)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize(
    "chunk_count, ret_chunk_count",
    [[0, (1, 1)], [1, (1, 1)], [2, (2, 2)], [3, (3, 2)], [4, (3, 4)], [9, (6, 4)]],
)
def test_chunk_count_1d(
    xyz_7x5_as_arrays: tuple[CoordinateArray, ...],
    name: str,
    chunk_count: int,
    ret_chunk_count: tuple[int, int],
) -> None:
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contour_generator(x, y, z, name=name, chunk_count=chunk_count)
    ret_y_chunk_size, ret_x_chunk_size = cont_gen.chunk_size
    assert cont_gen.chunk_count == ret_chunk_count
    ret_y_chunk_count, ret_x_chunk_count = ret_chunk_count
    assert ret_y_chunk_count*ret_y_chunk_size >= ny-1
    assert (ret_y_chunk_count-1)*ret_y_chunk_size < ny-1
    assert ret_x_chunk_count*ret_x_chunk_size >= nx-1
    assert (ret_x_chunk_count-1)*ret_x_chunk_size < nx-1


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize(
    "chunk_count, ret_chunk_count",
    [[(0, 1), (1, 1)], [(1, 0), (1, 1)], [(2, 3), (2, 2)], [(3, 2), (3, 2)], [(1, 9), (1, 4)],
     [(9, 1), (6, 1)]],
)
def test_chunk_count_2d(
    xyz_7x5_as_arrays: tuple[CoordinateArray, ...],
    name: str,
    chunk_count: tuple[int, int],
    ret_chunk_count: tuple[int, int],
) -> None:
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contour_generator(x, y, z, name=name, chunk_count=chunk_count)
    ret_y_chunk_size, ret_x_chunk_size = cont_gen.chunk_size
    assert cont_gen.chunk_count == ret_chunk_count
    ret_y_chunk_count, ret_x_chunk_count = ret_chunk_count
    assert ret_y_chunk_count*ret_y_chunk_size >= ny-1
    assert (ret_y_chunk_count-1)*ret_y_chunk_size < ny-1
    assert ret_x_chunk_count*ret_x_chunk_size >= nx-1
    assert (ret_x_chunk_count-1)*ret_x_chunk_size < nx-1


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize(
    "total_chunk_count, ret_chunk_count",
    [[0, (1, 1)], [1, (1, 1)], [2, (2, 1)], [3, (3, 1)], [4, (2, 2)], [6, (3, 2)], [9, (3, 2)],
     [25, (6, 4)]],
)
def test_total_chunk_count(
    xyz_7x5_as_arrays: tuple[CoordinateArray, ...],
    name: str,
    total_chunk_count: int,
    ret_chunk_count: tuple[int, int],
) -> None:
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contour_generator(x, y, z, name=name, total_chunk_count=total_chunk_count)
    ret_y_chunk_size, ret_x_chunk_size = cont_gen.chunk_size
    assert cont_gen.chunk_count == ret_chunk_count
    ret_y_chunk_count, ret_x_chunk_count = ret_chunk_count
    assert ret_y_chunk_count*ret_y_chunk_size >= ny-1
    assert (ret_y_chunk_count-1)*ret_y_chunk_size < ny-1
    assert ret_x_chunk_count*ret_x_chunk_size >= nx-1
    assert (ret_x_chunk_count-1)*ret_x_chunk_size < nx-1


def test_name_invalid(xyz_3x3_as_lists: tuple[list[list[int]], ...]) -> None:
    x, y, z = xyz_3x3_as_lists
    name = "some invalid name"
    msg = f"Unrecognised contour generator name: {name}"
    with pytest.raises(ValueError, match=msg):
        _ = contour_generator(x, y, z, name=name)


@pytest.mark.parametrize("name", ["mpl2005", "mpl2014"])
@pytest.mark.parametrize(
    "line_type", [LineType.Separate, LineType.ChunkCombinedCode, LineType.ChunkCombinedOffset])
def test_line_type_not_supported(
    xyz_3x3_as_lists: tuple[list[list[int]], ...],
    name: str,
    line_type: LineType,
) -> None:
    x, y, z = xyz_3x3_as_lists
    msg = f"{name} contour generator does not support line_type {line_type}"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, line_type=line_type)


@pytest.mark.parametrize("name", ["mpl2005", "mpl2014"])
@pytest.mark.parametrize("fill_type", [
    FillType.OuterOffset, FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset,
    FillType.ChunkCombinedCodeOffset, FillType.ChunkCombinedOffsetOffset])
def test_fill_type_not_supported(
    xyz_3x3_as_lists: tuple[list[list[int]], ...],
    name: str,
    fill_type: FillType,
) -> None:
    x, y, z = xyz_3x3_as_lists
    msg = f"{name} contour generator does not support fill_type {fill_type}"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, fill_type=fill_type)


@pytest.mark.parametrize("name", util_test.all_names())
def test_properties(xyz_3x3_as_lists: tuple[list[list[int]], ...], name: str) -> None:
    # Test that each ContourGenerator class implements all the required properties.
    x, y, z = xyz_3x3_as_lists
    cont_gen = contour_generator(x, y, z, name=name)
    _, _ = cont_gen.chunk_count
    _, _ = cont_gen.chunk_size
    _ = cont_gen.corner_mask
    _ = cont_gen.fill_type
    _ = cont_gen.line_type
    _ = cont_gen.quad_as_tri
    _ = cont_gen.thread_count
    _ = cont_gen.z_interp


@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_quad_as_tri(xyz_3x3_as_lists: tuple[list[list[int]], ...], name: str) -> None:
    x, y, z = xyz_3x3_as_lists
    for quad_as_tri in [False, True]:
        cont_gen = contour_generator(x, y, z, name=name, quad_as_tri=quad_as_tri)
        assert cont_gen.quad_as_tri == quad_as_tri


def test_quad_as_tri_not_supported(xyz_3x3_as_lists: tuple[list[list[int]], ...]) -> None:
    x, y, z = xyz_3x3_as_lists
    name = "mpl2005"
    msg = f"{name} contour generator does not support quad_as_tri=True"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, quad_as_tri=True)


@pytest.mark.parametrize("chunk_size", [0, 1, 2])
@pytest.mark.parametrize("thread_count", [0, 1, 2])
def test_thread_count(
    xyz_7x5_as_arrays: tuple[CoordinateArray, ...],
    chunk_size: int,
    thread_count: int,
) -> None:
    name = "threaded"
    x, y, z = xyz_7x5_as_arrays
    cont_gen = contour_generator(
        x, y, z, name=name, chunk_size=chunk_size, thread_count=thread_count)
    ret_thread_count = cont_gen.thread_count
    ret_chunk_count = math.prod(cont_gen.chunk_count)
    max_thread_count = max_threads()
    if chunk_size == 0:
        assert ret_chunk_count == 1
        assert ret_thread_count == 1
    elif thread_count == 0:
        assert ret_thread_count == min(max_thread_count, ret_chunk_count)
    else:
        assert ret_thread_count == min(max_thread_count, ret_chunk_count, ret_thread_count)


@pytest.mark.parametrize("name", util_test.all_names(exclude="threaded"))
def test_thread_count_not_supported(
    xyz_3x3_as_lists: tuple[list[list[int]], ...],
    name: str,
) -> None:
    x, y, z = xyz_3x3_as_lists
    thread_count = 2
    msg = f"{name} contour generator does not support thread_count {thread_count}"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, thread_count=thread_count)


def test_enums_as_strings(xyz_3x3_as_lists: tuple[list[list[int]], ...]) -> None:
    x, y, z = xyz_3x3_as_lists
    cg = contour_generator(
        x, y, z, line_type="SeparateCode", fill_type="ChunkCombinedCodeOffset", z_interp="Log")
    assert cg.line_type == LineType.SeparateCode
    assert cg.fill_type == FillType.ChunkCombinedCodeOffset
    assert cg.z_interp == ZInterp.Log


@pytest.mark.parametrize("name", util_test.all_names())
def test_is_contour_generator(name: str, xyz_3x3_as_lists: tuple[list[list[int]], ...]) -> None:
    x, y, z = xyz_3x3_as_lists
    cg = contour_generator(x, y, z, name=name)
    assert isinstance(cg, ContourGenerator)


@pytest.mark.parametrize("name", util_test.all_names())
def test_z_interp_none_to_linear(name: str, xyz_3x3_as_lists: tuple[list[list[int]], ...]) -> None:
    x, y, z = xyz_3x3_as_lists
    cg = contour_generator(x, y, z, name=name, z_interp=None)
    assert cg.z_interp == ZInterp.Linear


@pytest.mark.parametrize("name", ["mpl2005", "mpl2014"])
def test_z_interp_not_supported(name: str, xyz_3x3_as_lists: tuple[list[list[int]], ...]) -> None:
    x, y, z = xyz_3x3_as_lists
    msg = f"{name} contour generator does not support z_interp ZInterp.Log"
    with pytest.raises(ValueError, match=msg):
        contour_generator(x, y, z, name=name, z_interp=ZInterp.Log)
