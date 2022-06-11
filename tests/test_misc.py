import numpy as np

from contourpy import _remove_z_mask, max_threads


def test_max_threads():
    n = max_threads()
    # Assume testing on machine with 2 or more cores.
    assert n > 1


def test_remove_z_mask():
    zlist = [[1.0, 2.0], [3.0, 4.0]]

    zz, mask = _remove_z_mask(zlist)
    assert isinstance(zz, np.ndarray)
    assert mask is None

    zarr = np.asarray(zlist)
    zz, mask = _remove_z_mask(zarr)
    assert isinstance(zz, np.ndarray)
    assert mask is None

    z = np.ma.array(zlist, mask=[[0, 0], [0, 0]])
    zz, mask = _remove_z_mask(zarr)
    assert isinstance(zz, np.ndarray)
    assert mask is None

    z = np.ma.array(zlist, mask=[[1, 0], [0, 0]])
    zz, mask = _remove_z_mask(z)
    assert isinstance(zz, np.ndarray)
    assert isinstance(mask, np.ndarray)
    assert mask.dtype == bool
    np.testing.assert_array_equal(mask, [[True, False], [False, False]])

    z = [[1.0, np.nan], [2.0, np.inf]]
    zz, mask = _remove_z_mask(z)
    assert isinstance(zz, np.ndarray)
    assert isinstance(mask, np.ndarray)
    assert mask.dtype == bool
    np.testing.assert_array_equal(mask, [[False, True], [False, True]])

    z = np.ma.array(zlist, mask=[[1, 0], [0, 0]])
    z[1][1] = np.nan
    zz, mask = _remove_z_mask(z)
    assert isinstance(zz, np.ndarray)
    assert isinstance(mask, np.ndarray)
    assert mask.dtype == bool
    np.testing.assert_array_equal(mask, [[True, False], [False, True]])
