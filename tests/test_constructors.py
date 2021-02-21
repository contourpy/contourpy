import contourpy
import numpy as np
import pytest


@pytest.fixture
def xyz_as_lists():
    x = [[0, 0], [1, 1]]
    y = [[0, 1], [0, 1]]
    z = [[0, 1], [2, 3]]
    return x, y, z


@pytest.mark.parametrize('x', ( [1], [[[1]]] ))
def test_wrapper_ndim_x(xyz_as_lists, x):
    _, y_ok, z_ok = xyz_as_lists
    with pytest.raises(ValueError, match='x, y and z must all be 2D arrays'):
        cont_gen = contourpy.contour_generator(x, y_ok, z_ok)


@pytest.mark.parametrize('y', ( [1], [[[1]]] ))
def test_wrapper_ndim_y(xyz_as_lists, y):
    x_ok, _, z_ok = xyz_as_lists
    with pytest.raises(ValueError, match='x, y and z must all be 2D arrays'):
        cont_gen = contourpy.contour_generator(x_ok, y, z_ok)


@pytest.mark.parametrize('z', ( [1], [[[1]]] ))
def test_wrapper_ndim_z(xyz_as_lists, z):
    x_ok, y_ok, _ = xyz_as_lists
    with pytest.raises(ValueError, match='x, y and z must all be 2D arrays'):
        cont_gen = contourpy.contour_generator(x_ok, y_ok, z)


@pytest.mark.parametrize('diff_shape', ( [[1, 2, 3], [4, 5, 6]],
                                         [[1, 2], [3, 4], [5, 6]] ))
def test_wrapper_diff_shapes(xyz_as_lists, diff_shape):
    x_ok, y_ok, z_ok = xyz_as_lists

    with pytest.raises(ValueError, match='x, y and z arrays must have the same shape'):
        cont_gen = contourpy.contour_generator(diff_shape, y_ok, z_ok)

    with pytest.raises(ValueError, match='x, y and z arrays must have the same shape'):
        cont_gen = contourpy.contour_generator(x_ok, diff_shape, z_ok)

    with pytest.raises(ValueError, match='x, y and z arrays must have the same shape'):
        cont_gen = contourpy.contour_generator(x_ok, y_ok, diff_shape)


@pytest.mark.parametrize('all_xyz', ( [[1]], [[1], [2]], [[1, 2]] ))
def test_wrapper_shape_too_small(all_xyz):
    with pytest.raises(ValueError, match='x, y and z must all be at least 2x2 arrays'):
        cont_gen = contourpy.contour_generator(all_xyz, all_xyz, all_xyz)


def test_wrapper_chunk_size_negative(xyz_as_lists):
    x, y, z = xyz_as_lists
    with pytest.raises(ValueError, match='chunk_size cannot be negative'):
        cont_gen = contourpy.contour_generator(x, y, z, chunk_size=-1)
