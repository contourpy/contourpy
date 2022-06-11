import numpy as np
import pytest

import contourpy

from . import util_test


@pytest.fixture
def xyz_3x3_as_lists():
    x = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    y = [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
    z = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return x, y, z


@pytest.fixture
def xyz_2x3_as_lists():  # shape (2, 3)
    x = [[0, 1, 2], [0, 1, 2]]
    y = [[0, 0, 0], [1, 1, 1]]
    z = [[0, 1, 2], [3, 4, 5]]
    return x, y, z


@pytest.fixture
def xyz_7x5_as_arrays():  # shape (7, 5)
    x, y = np.meshgrid([0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5, 6])
    z = x + y
    return x, y, z


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("z", ([1], [[[1]]]))
def test_ndim_z(xyz_3x3_as_lists, name, z):
    x, y, _ = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        contourpy.contour_generator(x, y, z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("all_xyz", ([[1]], [[1], [2]], [[1, 2]]))
def test_z_shape_too_small(all_xyz, name):
    with pytest.raises(TypeError):
        contourpy.contour_generator(all_xyz, all_xyz, all_xyz, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("wrong_ndim", (None, [1], [[[1]]]))
def test_diff_ndim_xy(xyz_3x3_as_lists, name, wrong_ndim):
    x, y, z = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        contourpy.contour_generator(wrong_ndim, y, z, name=name)
    with pytest.raises(TypeError):
        contourpy.contour_generator(x, wrong_ndim, z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_xy_None(xyz_3x3_as_lists, name):
    _, _, z = xyz_3x3_as_lists
    contourpy.contour_generator(None, None, z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_xy_not_specified(xyz_3x3_as_lists, name):
    _, _, z = xyz_3x3_as_lists
    contourpy.contour_generator(z=z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_xy_1d(name):
    z = [[0, 1, 2], [3, 4, 5]]
    contourpy.contour_generator([0, 1, 2], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        contourpy.contour_generator([0, 1], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        contourpy.contour_generator([0, 1, 2, 3], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        contourpy.contour_generator([0, 1, 2], [0], z, name=name)
    with pytest.raises(TypeError):
        contourpy.contour_generator([0, 1, 2], [0, 1, 2], z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("diff_shape", ([[1, 2, 3, 4], [5, 6, 7, 8]], [[1, 2], [3, 4], [5, 6]]))
def test_xyz_diff_shapes(xyz_3x3_as_lists, name, diff_shape):
    x, y, z = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        contourpy.contour_generator(diff_shape, y, z, name=name)
    with pytest.raises(TypeError):
        contourpy.contour_generator(x, diff_shape, z, name=name)
    with pytest.raises(TypeError):
        contourpy.contour_generator(x, y, diff_shape, name=name)


@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_corner_mask(xyz_3x3_as_lists, name):
    x, y, z = xyz_3x3_as_lists
    for corner_mask in [False, True]:
        cont_gen = contourpy.contour_generator(x, y, z, name=name, corner_mask=corner_mask)
        assert cont_gen.corner_mask == corner_mask


@pytest.mark.parametrize('name', util_test.all_names())
def test_chunk_size_negative(xyz_3x3_as_lists, name):
    x, y, z = xyz_3x3_as_lists
    msg = "chunk_size cannot be negative"
    with pytest.raises(ValueError, match=msg):
        contourpy.contour_generator(x, y, z, name=name, chunk_size=-1)
    with pytest.raises(ValueError, match=msg):
        contourpy.contour_generator(x, y, z, name=name, chunk_size=(-1, 0))
    with pytest.raises(ValueError, match=msg):
        contourpy.contour_generator(x, y, z, name=name, chunk_size=(0, -1))


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("chunk_size", np.arange(9))
def test_chunk_size_1d(xyz_7x5_as_arrays, name, chunk_size):
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_size=chunk_size)
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
def test_chunk_size_2d(xyz_7x5_as_arrays, name, x_chunk_size, y_chunk_size):
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contourpy.contour_generator(
        x, y, z, name=name, chunk_size=(y_chunk_size, x_chunk_size))
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


def test_chunk_size_and_count(xyz_7x5_as_arrays):
    x, y, z = xyz_7x5_as_arrays
    name = "serial"
    msg = "Only one of chunk_size, chunk_count and total_chunk_count should be set"
    with pytest.raises(ValueError, match=msg):
        contourpy.contour_generator(x, y, z, name=name, chunk_size=1, chunk_count=1)
    with pytest.raises(ValueError, match=msg):
        contourpy.contour_generator(x, y, z, name=name, chunk_size=1, total_chunk_count=1)
    with pytest.raises(ValueError, match=msg):
        contourpy.contour_generator(x, y, z, name=name, chunk_count=1, total_chunk_count=1)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize(
    "chunk_count, ret_chunk_count",
    [[0, (1, 1)], [1, (1, 1)], [2, (2, 2)], [3, (3, 2)], [4, (3, 4)], [9, (6, 4)]],
)
def test_chunk_count_1d(xyz_7x5_as_arrays, name, chunk_count, ret_chunk_count):
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_count=chunk_count)
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
def test_chunk_count_2d(xyz_7x5_as_arrays, name, chunk_count, ret_chunk_count):
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_count=chunk_count)
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
def test_total_chunk_count(xyz_7x5_as_arrays, name, total_chunk_count, ret_chunk_count):
    x, y, z = xyz_7x5_as_arrays
    ny, nx = z.shape
    cont_gen = contourpy.contour_generator(x, y, z, name=name, total_chunk_count=total_chunk_count)
    ret_y_chunk_size, ret_x_chunk_size = cont_gen.chunk_size
    assert cont_gen.chunk_count == ret_chunk_count
    ret_y_chunk_count, ret_x_chunk_count = ret_chunk_count
    assert ret_y_chunk_count*ret_y_chunk_size >= ny-1
    assert (ret_y_chunk_count-1)*ret_y_chunk_size < ny-1
    assert ret_x_chunk_count*ret_x_chunk_size >= nx-1
    assert (ret_x_chunk_count-1)*ret_x_chunk_size < nx-1


def test_name_invalid(xyz_3x3_as_lists):
    x, y, z = xyz_3x3_as_lists
    name = "some invalid name"
    msg = f"Unrecognised contour generator name: {name}"
    with pytest.raises(ValueError, match=msg):
        _ = contourpy.contour_generator(x, y, z, name=name)


@pytest.mark.parametrize("name", util_test.all_names())
def test_properties(xyz_3x3_as_lists, name):
    # Test that each ContourGenerator class implements all the required properties.
    x, y, z = xyz_3x3_as_lists
    cont_gen = contourpy.contour_generator(x, y, z, name=name)
    _, _ = cont_gen.chunk_count
    _, _ = cont_gen.chunk_size
    _ = cont_gen.corner_mask
    _ = cont_gen.fill_type
    _ = cont_gen.line_type
    _ = cont_gen.quad_as_tri
    _ = cont_gen.thread_count
    _ = cont_gen.z_interp


@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_quad_as_tri(xyz_3x3_as_lists, name):
    x, y, z = xyz_3x3_as_lists
    for quad_as_tri in [False, True]:
        cont_gen = contourpy.contour_generator(x, y, z, name=name, quad_as_tri=quad_as_tri)
        assert cont_gen.quad_as_tri == quad_as_tri


@pytest.mark.parametrize("chunk_size", [0, 1, 2])
@pytest.mark.parametrize("thread_count", [0, 1, 2])
def test_thread_count(xyz_7x5_as_arrays, chunk_size, thread_count):
    name = "threaded"
    x, y, z = xyz_7x5_as_arrays
    cont_gen = contourpy.contour_generator(
        x, y, z, name=name, chunk_size=chunk_size, thread_count=thread_count)
    ret_thread_count = cont_gen.thread_count
    ret_chunk_count = np.prod(cont_gen.chunk_count)
    max_threads = contourpy.max_threads()
    if chunk_size == 0:
        assert ret_chunk_count == 1
        assert ret_thread_count == 1
    elif thread_count == 0:
        assert ret_thread_count == min(max_threads, ret_chunk_count)
    else:
        assert ret_thread_count == min(max_threads, ret_chunk_count, ret_thread_count)


def test_enums_as_strings(xyz_3x3_as_lists):
    x, y, z = xyz_3x3_as_lists
    cg = contourpy.contour_generator(
        x, y, z, line_type="SeparateCode", fill_type="ChunkCombinedCodeOffset", z_interp="Log")
    assert cg.line_type == contourpy.LineType.SeparateCode
    assert cg.fill_type == contourpy.FillType.ChunkCombinedCodeOffset
    assert cg.z_interp == contourpy.ZInterp.Log


@pytest.mark.parametrize("name", util_test.all_names())
def test_is_contour_generator(name, xyz_3x3_as_lists):
    x, y, z = xyz_3x3_as_lists
    cg = contourpy.contour_generator(x, y, z, name=name)
    assert isinstance(cg, contourpy.ContourGenerator)
