import contourpy
import numpy as np
import pytest
import re
import util_test


@pytest.fixture
def xyz_as_lists():
    x = [[0, 1, 2], [0, 1, 2]]
    y = [[0, 0, 0], [1, 1, 1]]
    z = [[0, 1, 2], [3, 4, 5]]
    return x, y, z



@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('z', ( [1], [[[1]]] ))
def test_ndim_z(xyz_as_lists, name, z):
    x, y, _ = xyz_as_lists
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, y, z, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('all_xyz', ( [[1]], [[1], [2]], [[1, 2]] ))
def test_z_shape_too_small(all_xyz, name):
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(all_xyz, all_xyz, all_xyz, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
@pytest.mark.parametrize('wrong_ndim', ( None, [1], [[[1]]] ))
def test_diff_ndim_xy(xyz_as_lists, name, wrong_ndim):
    x, y, z = xyz_as_lists
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(wrong_ndim, y, z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, wrong_ndim, z, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
def test_xy_None(xyz_as_lists, name):
    _, _, z = xyz_as_lists
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
def test_wrapper_diff_shapes(xyz_as_lists, name, diff_shape):
    x, y, z = xyz_as_lists
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(diff_shape, y, z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, diff_shape, z, name=name)
    with pytest.raises(TypeError):
        cont_gen = contourpy.contour_generator(x, y, diff_shape, name=name)


@pytest.mark.parametrize('name', util_test.all_names())
def test_chunk_size_negative(xyz_as_lists, name):
    x, y, z = xyz_as_lists
    with pytest.raises(ValueError, match='chunk_size cannot be negative'):
        cont_gen = contourpy.contour_generator(x, y, z, name=name, chunk_size=-1)
