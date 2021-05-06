import contourpy
import numpy as np
import pytest
import re
import util_test


@pytest.fixture
def xyz_3x3_as_lists():
    x = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    y = [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
    z = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    return x, y, z


@pytest.fixture
def xyz_2x3_as_lists():  # shape (2,3)
    x = [[0, 1, 2], [0, 1, 2]]
    y = [[0, 0, 0], [1, 1, 1]]
    z = [[0, 1, 2], [3, 4, 5]]
    return x, y, z


@pytest.fixture
def xyz_5x5_as_arrays():
    x, y = np.meshgrid([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    z = x + y
    return x, y, z


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('z', ( [1], [[[1]]] ))
def test_ndim_z(xyz_3x3_as_lists, name, z):
    x, y, _ = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, y, z, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('all_xyz', ( [[1]], [[1], [2]], [[1, 2]] ))
def test_z_shape_too_small(all_xyz, name):
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(all_xyz, all_xyz, all_xyz, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('wrong_ndim', ( None, [1], [[[1]]] ))
def test_diff_ndim_xy(xyz_3x3_as_lists, name, wrong_ndim):
    x, y, z = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(wrong_ndim, y, z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, wrong_ndim, z, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
def test_xy_None(xyz_3x3_as_lists, name):
    _, _, z = xyz_3x3_as_lists
    cont_gen = contourpy.contour_generator(None, None, z, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
def test_xy_1d(name):
    z = [[0, 1, 2], [3, 4, 5]]
    cont_gen = contourpy.contour_generator([0, 1, 2], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator([0, 1], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator([0, 1, 2, 3], [0, 1], z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator([0, 1, 2], [0], z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator([0, 1, 2], [0, 1, 2], z, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('diff_shape', ( [[1, 2, 3, 4], [5, 6, 7, 8]],
                                         [[1, 2], [3, 4], [5, 6]] ))
def test_wrapper_diff_shapes(xyz_3x3_as_lists, name, diff_shape):
    x, y, z = xyz_3x3_as_lists
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(diff_shape, y, z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, diff_shape, z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, y, diff_shape, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
def test_chunk_size_negative(xyz_3x3_as_lists, name):
    x, y, z = xyz_3x3_as_lists
    with pytest.raises(ValueError, match='chunk_size cannot be negative'):
        cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_size=-1)
    with pytest.raises(ValueError, match='chunk_size cannot be negative'):
        cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_size=(-1, 0))
    with pytest.raises(ValueError, match='chunk_size cannot be negative'):
        cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_size=(0, -1))


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('chunk_size', [0, 1, 2, 10])
def test_chunk_size_1d(xyz_2x3_as_lists, name, chunk_size):
    x, y, z = xyz_2x3_as_lists
    ny, nx = 2, 3
    cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_size=chunk_size)
    if name == 'mpl2005':
        pytest.skip()  # Doesn't have chunk_size property.
    ret_chunk_size = cont_gen.chunk_size
    if chunk_size == 0:
        assert ret_chunk_size[0] == ny-1
        assert ret_chunk_size[1] == nx-1
    else:
        assert ret_chunk_size[0] == min(chunk_size, ny-1)
        assert ret_chunk_size[1] == min(chunk_size, nx-1)


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('x_chunk_size', [0, 1, 2, 10])
@pytest.mark.parametrize('y_chunk_size', [0, 1, 2, 10])
def test_chunk_size_2d(xyz_2x3_as_lists, name, x_chunk_size, y_chunk_size):
    x, y, z = xyz_2x3_as_lists
    ny, nx = 2, 3
    cont_gen = contourpy.contour_generator(
        x, y, z, name=name, chunk_size=(y_chunk_size, x_chunk_size))
    if name == 'mpl2005':  # Doesn't have chunk_size property.
        pytest.skip()
    ret_y_chunk_size, ret_x_chunk_size = cont_gen.chunk_size
    if x_chunk_size == 0:
        assert ret_x_chunk_size == nx-1
    else:
        assert ret_x_chunk_size == min(x_chunk_size, nx-1)
    if y_chunk_size == 0:
        assert ret_y_chunk_size == ny-1
    else:
        assert ret_y_chunk_size == min(y_chunk_size, ny-1)


@pytest.mark.parametrize('chunk_size', [0, 1, 2])
@pytest.mark.parametrize('thread_count', [0, 1, 2])
def test_thread_count(xyz_5x5_as_arrays, chunk_size, thread_count):
    name = 'threaded'
    x, y, z = xyz_5x5_as_arrays
    cont_gen = contourpy.contour_generator(
        x, y, z, name=name, chunk_size=chunk_size, thread_count=thread_count)
    ret_thread_count = cont_gen.thread_count
    ret_chunk_count = np.prod(cont_gen.chunk_count)
    ret_max_threads = cont_gen.max_threads  
    if chunk_size == 0:
        assert ret_chunk_count == 1
        assert ret_thread_count == 1
    elif thread_count == 0:
        assert ret_thread_count == min(ret_max_threads, ret_chunk_count)
    else:
        assert ret_thread_count == min(ret_max_threads, ret_chunk_count, ret_thread_count)
