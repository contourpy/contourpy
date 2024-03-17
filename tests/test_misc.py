from __future__ import annotations

import numpy as np

from contourpy import _remove_z_mask, contour_generator


def test_nan() -> None:
    # Test that the nan used by contourpy is numpy.nan.
    cont_gen = contour_generator(z=[[0, 1], [1, 0]], line_type="ChunkCombinedNan")
    lines = cont_gen.lines(0.5)
    assert lines[0][0] is not None
    assert np.all(np.isnan(lines[0][0][2, :]))


def test_remove_z_mask() -> None:
    zlist = [[1.0, 2.0], [3.0, 4.0]]

    zz, mask = _remove_z_mask(zlist)
    assert isinstance(zz, np.ndarray)
    assert mask is None

    zarr = np.asarray(zlist)
    zz, mask = _remove_z_mask(zarr)
    assert isinstance(zz, np.ndarray)
    assert mask is None

    z = np.ma.array(zlist, mask=[[0, 0], [0, 0]])  # type: ignore[no-untyped-call]
    zz, mask = _remove_z_mask(zarr)
    assert isinstance(zz, np.ndarray)
    assert mask is None

    z = np.ma.array(zlist, mask=[[1, 0], [0, 0]])  # type: ignore[no-untyped-call]
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

    z = np.ma.array(zlist, mask=[[1, 0], [0, 0]])  # type: ignore[no-untyped-call]
    z[1][1] = np.nan
    zz, mask = _remove_z_mask(z)
    assert isinstance(zz, np.ndarray)
    assert isinstance(mask, np.ndarray)
    assert mask.dtype == bool
    np.testing.assert_array_equal(mask, [[True, False], [False, True]])
