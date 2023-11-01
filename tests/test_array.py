from __future__ import annotations

import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
import pytest

import contourpy.array as arr
from contourpy.types import code_dtype, offset_dtype, point_dtype

from . import util_test


def test_codes_from_offsets() -> None:
    codes = arr.codes_from_offsets(np.array([0, 3], dtype=offset_dtype))
    util_test.assert_code_array(codes, 3)
    assert_array_equal(codes, [1, 2, 79])

    codes = arr.codes_from_offsets(np.array([0, 3, 7], dtype=offset_dtype))
    util_test.assert_code_array(codes, 7)
    assert_array_equal(codes, [1, 2, 79, 1, 2, 2, 79])

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.codes_from_offsets([0, 3, 7])  # type: ignore[arg-type]

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint32'>"):
        arr.codes_from_offsets(np.array([0, 3, 7], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.codes_from_offsets(np.array([[0, 3], [7, 10]], dtype=offset_dtype))

    with pytest.raises(ValueError, match=r"First element of offset array must be 0"):
        arr.codes_from_offsets(np.array([1, 2], dtype=offset_dtype))


def test_codes_from_offsets_and_points() -> None:
    codes = arr.codes_from_offsets_and_points(
        np.array([0, 3], dtype=offset_dtype),
        np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype),
    )
    util_test.assert_code_array(codes, 3)
    assert_array_equal(codes, [1, 2, 2])

    codes = arr.codes_from_offsets_and_points(
        np.array([0, 3], dtype=offset_dtype),
        np.array([[0, 1], [2, 3], [0, 1]], dtype=point_dtype),
    )
    util_test.assert_code_array(codes, 3)
    assert_array_equal(codes, [1, 2, 79])

    codes = arr.codes_from_offsets_and_points(
        np.array([0, 3, 7], dtype=offset_dtype),
        np.array([[0, 1], [2, 3], [0, 1], [5, 6], [7, 8], [9, 10], [5, 6]], dtype=point_dtype),
    )
    util_test.assert_code_array(codes, 7)
    assert_array_equal(codes, [1, 2, 79, 1, 2, 2, 79])

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.codes_from_offsets_and_points(
            [0, 2],  # type: ignore[arg-type]
            np.array([[0, 1], [2, 3]], dtype=point_dtype),
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint32'>"):
        arr.codes_from_offsets_and_points(
            np.array([0, 2], dtype=np.int64),
            np.array([[0, 1], [2, 3]], dtype=point_dtype),
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.codes_from_offsets_and_points(
            np.array([[0], [2]], dtype=offset_dtype),
            np.array([[0, 1], [2, 3]], dtype=point_dtype),
        )

    with pytest.raises(ValueError, match=r"First element of offset array must be 0"):
        arr.codes_from_offsets_and_points(
            np.array([1, 2], dtype=offset_dtype),
            np.array([[0, 1], [2, 3]], dtype=point_dtype),
        )

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.codes_from_offsets_and_points(
            np.array([0, 2],
            dtype=offset_dtype), [[0, 1], [2, 3]],  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.float64'>"):
        arr.codes_from_offsets_and_points(
            np.array([0, 2], dtype=offset_dtype),
            np.array([[0, 1], [2, 3]], dtype=np.float32),
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.codes_from_offsets_and_points(
            np.array([0, 2], dtype=offset_dtype),
            np.array([0, 1, 2, 3], dtype=point_dtype),
        )


def test_codes_from_points() -> None:
    codes = arr.codes_from_points(np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype))
    util_test.assert_code_array(codes, 3)
    assert_array_equal(codes, [1, 2, 2])

    codes = arr.codes_from_points(np.array([[0, 1], [2, 3], [0, 1]], dtype=point_dtype))
    util_test.assert_code_array(codes, 3)
    assert_array_equal(codes, [1, 2, 79])

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.codes_from_points([[0, 1], [2, 3], [0, 1]])  # type: ignore[arg-type]

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.float64'>"):
        arr.codes_from_points(np.array([[0, 1], [2, 3], [4, 5]], dtype=np.float32))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.codes_from_points(np.array([0, 1, 2, 3], dtype=point_dtype))


def test_concat_codes() -> None:
    codes0 = np.array([1, 2, 79], dtype=code_dtype)
    codes1 = np.array([1, 2, 2, 2], dtype=code_dtype)

    codes = arr.concat_codes([codes0])
    util_test.assert_code_array(codes, 3)
    assert_array_equal(codes, codes0)

    codes = arr.concat_codes([codes1])
    util_test.assert_code_array(codes, 4)
    assert_array_equal(codes, codes1)

    codes = arr.concat_codes([codes0, codes1])
    util_test.assert_code_array(codes, 7)
    assert_array_equal(codes, [1, 2, 79, 1, 2, 2, 2])

    codes = arr.concat_codes([codes1, codes0])
    util_test.assert_code_array(codes, 7)
    assert_array_equal(codes, [1, 2, 2, 2, 1, 2, 79])

    with pytest.raises(ValueError, match=r"Empty list passed to concat_codes"):
        arr.concat_codes([])


def test_concat_codes_or_none() -> None:
    codes0 = np.array([1, 2, 79], dtype=code_dtype)
    codes1 = np.array([1, 2, 2, 2], dtype=code_dtype)

    assert arr.concat_codes_or_none([None]) is None
    assert arr.concat_codes_or_none([None, None]) is None
    assert arr.concat_codes_or_none([None, None, None]) is None

    codes = arr.concat_codes_or_none([None, codes0, None])
    assert codes is not None
    util_test.assert_code_array(codes, 3)
    assert_array_equal(codes, [1, 2, 79])

    codes = arr.concat_codes_or_none([None, codes0, None, codes1, None])
    assert codes is not None
    util_test.assert_code_array(codes, 7)
    assert_array_equal(codes, [1, 2, 79, 1, 2, 2, 2])

    codes = arr.concat_codes_or_none([None, codes1, None, codes0, None])
    assert codes is not None
    util_test.assert_code_array(codes, 7)
    assert_array_equal(codes, [1, 2, 2, 2, 1, 2, 79])


def test_concat_offsets() -> None:
    offsets0 = np.array([0, 2, 5], dtype=offset_dtype)
    offsets1 = np.array([0, 3, 7], dtype=offset_dtype)
    offsets2 = np.array([0, 4, 8], dtype=offset_dtype)

    offsets = arr.concat_offsets([offsets0, offsets1])
    util_test.assert_offset_array(offsets, 12)
    assert_array_equal(offsets, [0, 2, 5, 8, 12])

    offsets = arr.concat_offsets([offsets0, offsets1, offsets2])
    util_test.assert_offset_array(offsets, 20)
    assert_array_equal(offsets, [0, 2, 5, 8, 12, 16, 20])

    with pytest.raises(ValueError, match=r"Empty list passed to concat_offsets"):
        arr.concat_offsets([])


def test_concat_offsets_or_none() -> None:
    offsets0 = np.array([0, 2, 5], dtype=offset_dtype)
    offsets1 = np.array([0, 3, 7], dtype=offset_dtype)
    offsets2 = np.array([0, 4, 8], dtype=offset_dtype)

    assert arr.concat_offsets_or_none([None]) is None
    assert arr.concat_offsets_or_none([None, None]) is None
    assert arr.concat_offsets_or_none([None, None, None]) is None

    offsets = arr.concat_offsets_or_none([None, offsets0, None, offsets1, None])
    assert offsets is not None
    util_test.assert_offset_array(offsets, 12)
    assert_array_equal(offsets, [0, 2, 5, 8, 12])

    offsets = arr.concat_offsets_or_none([None, None, offsets0, offsets1, None, offsets2])
    assert offsets is not None
    util_test.assert_offset_array(offsets, 20)
    assert_array_equal(offsets, [0, 2, 5, 8, 12, 16, 20])


def test_concat_points() -> None:
    points0 = np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype)
    points1 = np.array([[6, 7], [8, 9]], dtype=point_dtype)

    points = arr.concat_points([points0])
    util_test.assert_point_array(points)
    assert_array_almost_equal(points, points0)

    points = arr.concat_points([points0, points1])
    util_test.assert_point_array(points)
    assert_array_almost_equal(
        points,
        np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]], dtype=point_dtype),
    )

    points = arr.concat_points([points1, points0])
    util_test.assert_point_array(points)
    assert_array_almost_equal(points, [[6, 7], [8, 9], [0, 1], [2, 3], [4, 5]])

    with pytest.raises(ValueError, match=r"Empty list passed to concat_points"):
        arr.concat_points([])


def test_concat_points_or_none() -> None:
    points0 = np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype)
    points1 = np.array([[6, 7], [8, 9]], dtype=point_dtype)

    assert arr.concat_points_or_none([None]) is None
    assert arr.concat_points_or_none([None, None]) is None
    assert arr.concat_points_or_none([None, None, None]) is None

    points = arr.concat_points_or_none([None, points0, None])
    assert points is not None
    util_test.assert_point_array(points)
    assert_array_almost_equal(points, points0)

    points = arr.concat_points_or_none([None, points0, None, points1, None])
    assert points is not None
    util_test.assert_point_array(points)
    assert_array_almost_equal(points, [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])

    points = arr.concat_points_or_none([None, None, points1, points0, None])
    assert points is not None
    util_test.assert_point_array(points)
    assert_array_almost_equal(points, [[6, 7], [8, 9], [0, 1], [2, 3], [4, 5]])


def test_concat_points_or_none_with_nan() -> None:
    points0 = np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype)
    points1 = np.array([[6, 7], [8, 9]], dtype=point_dtype)
    points2 = np.array([[-1, -2], [-3, -4]], dtype=point_dtype)

    assert arr.concat_points_or_none_with_nan([None]) is None
    assert arr.concat_points_or_none_with_nan([None, None]) is None
    assert arr.concat_points_or_none_with_nan([None, None, None]) is None

    points = arr.concat_points_or_none_with_nan([None, points0, None])
    assert points is not None
    util_test.assert_point_array(points)
    assert_array_almost_equal(points, points0)

    points = arr.concat_points_or_none_with_nan([None, points0, None, None, points1, None])
    assert points is not None
    util_test.assert_point_array(points, allow_nan=True)
    assert_array_almost_equal(
        points,
        np.array([[0, 1], [2, 3], [4, 5], [np.nan, np.nan], [6, 7], [8, 9]], dtype=point_dtype),
    )

    points = arr.concat_points_or_none_with_nan([None, points0, None, points1, None, None, points2])
    assert points is not None
    util_test.assert_point_array(points, allow_nan=True)
    assert_array_almost_equal(
        points,
        np.array([[0, 1], [2, 3], [4, 5], [np.nan, np.nan], [6, 7], [8, 9], [np.nan, np.nan],
                  [-1, -2], [-3, -4]], dtype=point_dtype),
    )


def test_concat_points_with_nan() -> None:
    points0 = np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype)
    points1 = np.array([[6, 7], [8, 9]], dtype=point_dtype)
    points2 = np.array([[-1, -2], [-3, -4]], dtype=point_dtype)

    points = arr.concat_points_with_nan([points0])
    util_test.assert_point_array(points)
    assert_array_almost_equal(points, points0)

    points = arr.concat_points_with_nan([points0, points1])
    util_test.assert_point_array(points, allow_nan=True)
    assert_array_almost_equal(
        points,
        np.array([[0, 1], [2, 3], [4, 5], [np.nan, np.nan], [6, 7], [8, 9]], dtype=point_dtype),
    )

    points = arr.concat_points_with_nan([points0, points1, points2])
    util_test.assert_point_array(points, allow_nan=True)
    assert_array_almost_equal(
        points,
        np.array([[0, 1], [2, 3], [4, 5], [np.nan, np.nan], [6, 7], [8, 9], [np.nan, np.nan],
                  [-1, -2], [-3, -4]], dtype=point_dtype),
    )

    with pytest.raises(ValueError, match=r"Empty list passed to concat_points_with_nan"):
        arr.concat_points_with_nan([])


def test_insert_nan_at_offsets() -> None:
    points0 = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]], dtype=point_dtype)

    points = arr.insert_nan_at_offsets(points0, np.array([0, 5], dtype=offset_dtype))
    util_test.assert_point_array(points, allow_nan=False)
    assert_array_almost_equal(points, points0)

    points = arr.insert_nan_at_offsets(points0, np.array([0, 1, 5], dtype=offset_dtype))
    util_test.assert_point_array(points, allow_nan=True)
    assert_array_almost_equal(
        points,
        np.array([[0, 1], [np.nan, np.nan], [2, 3], [4, 5], [6, 7], [8, 9]], dtype=point_dtype),
    )

    points = arr.insert_nan_at_offsets(points0, np.array([0, 1, 4, 5], dtype=offset_dtype))
    util_test.assert_point_array(points, allow_nan=True)
    assert_array_almost_equal(
        points,
        np.array([[0, 1], [np.nan, np.nan], [2, 3], [4, 5], [6, 7], [np.nan, np.nan], [8, 9]],
                 dtype=point_dtype),
    )

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.insert_nan_at_offsets(
            [[0, 1], [2, 3], [4, 5]],  # type: ignore[arg-type]
            np.array([0, 3], dtype=offset_dtype),
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.float64'>"):
        arr.insert_nan_at_offsets(
            np.array([[0, 1], [2, 3], [4, 5]], dtype=np.float32),
            np.array([0, 3], dtype=offset_dtype),
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.insert_nan_at_offsets(
            np.array([0, 1, 2, 3, 4, 5], dtype=point_dtype),
            np.array([0, 3], dtype=offset_dtype),
        )

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.insert_nan_at_offsets(
            np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype),
            [0, 3],  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint32'>"):
        arr.insert_nan_at_offsets(
            np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype),
            np.array([0, 3], dtype=np.int64),
        )

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.insert_nan_at_offsets(
            np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype),
            np.array([[0, 3]], dtype=offset_dtype),
        )

    with pytest.raises(ValueError, match=r"First element of offset array must be 0"):
        arr.insert_nan_at_offsets(
            np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype),
            np.array([1, 3], dtype=offset_dtype),
        )


def test_offsets_from_codes() -> None:
    offsets = arr.offsets_from_codes(np.array([1, 2, 79], dtype=code_dtype))
    util_test.assert_offset_array(offsets, 3)
    assert_array_equal(offsets, [0, 3])

    offsets = arr.offsets_from_codes(np.array([1, 2, 79, 1, 2, 2, 1, 2], dtype=code_dtype))
    util_test.assert_offset_array(offsets, 8)
    assert_array_equal(offsets, [0, 3, 6, 8])

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.offsets_from_codes([1, 2, 79])  # type: ignore[arg-type]

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint8'>"):
        arr.offsets_from_codes(np.array([1, 2, 79], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.offsets_from_codes(np.array([[1, 2], [2, 79]], dtype=code_dtype))

    with pytest.raises(ValueError, match=r"First element of code array must be 1"):
        arr.offsets_from_codes(np.array([2, 79], dtype=code_dtype))


def test_offsets_from_lengths() -> None:
    points0 = np.array([[0, 1], [2, 3], [4, 5]], dtype=point_dtype)
    points1 = np.array([[6, 7], [8, 9]], dtype=point_dtype)

    offsets = arr.offsets_from_lengths([points0])
    util_test.assert_offset_array(offsets, 3)
    assert_array_equal(offsets, [0, 3])

    offsets = arr.offsets_from_lengths([points0, points1])
    util_test.assert_offset_array(offsets, 5)
    assert_array_equal(offsets, [0, 3, 5])

    offsets = arr.offsets_from_lengths([points1, points0])
    util_test.assert_offset_array(offsets, 5)
    assert_array_equal(offsets, [0, 2, 5])

    with pytest.raises(ValueError, match=r"Empty list passed to offsets_from_lengths"):
        arr.offsets_from_lengths([])


def test_outer_offsets_from_list_of_codes() -> None:
    codes0 = np.array([1, 2, 79, 1, 2], dtype=code_dtype)
    codes1 = np.array([1, 2, 2, 2, 1, 2, 1, 2, 2], dtype=code_dtype)

    outer_offsets = arr.outer_offsets_from_list_of_codes([codes0])
    util_test.assert_offset_array(outer_offsets, 2)
    assert_array_equal(outer_offsets, [0, 2])

    outer_offsets = arr.outer_offsets_from_list_of_codes([codes1])
    util_test.assert_offset_array(outer_offsets, 3)
    assert_array_equal(outer_offsets, [0, 3])

    outer_offsets = arr.outer_offsets_from_list_of_codes([codes0, codes1])
    util_test.assert_offset_array(outer_offsets, 5)
    assert_array_equal(outer_offsets, [0, 2, 5])

    outer_offsets = arr.outer_offsets_from_list_of_codes([codes1, codes0])
    util_test.assert_offset_array(outer_offsets, 5)
    assert_array_equal(outer_offsets, [0, 3, 5])

    with pytest.raises(ValueError, match=r"Empty list passed to outer_offsets_from_list_of_codes"):
        arr.outer_offsets_from_list_of_codes([])


def test_outer_offsets_from_list_of_offsets() -> None:
    offsets0 = np.array([0, 3, 5], dtype=offset_dtype)
    offsets1 = np.array([0, 4, 9, 11], dtype=offset_dtype)

    outer_offsets = arr.outer_offsets_from_list_of_offsets([offsets0])
    util_test.assert_offset_array(outer_offsets, 2)
    assert_array_equal(outer_offsets, [0, 2])

    outer_offsets = arr.outer_offsets_from_list_of_offsets([offsets1])
    util_test.assert_offset_array(outer_offsets, 3)
    assert_array_equal(outer_offsets, [0, 3])

    outer_offsets = arr.outer_offsets_from_list_of_offsets([offsets0, offsets1])
    util_test.assert_offset_array(outer_offsets, 5)
    assert_array_equal(outer_offsets, [0, 2, 5])

    outer_offsets = arr.outer_offsets_from_list_of_offsets([offsets1, offsets0])
    util_test.assert_offset_array(outer_offsets, 5)
    assert_array_equal(outer_offsets, [0, 3, 5])

    with pytest.raises(ValueError,
                       match=r"Empty list passed to outer_offsets_from_list_of_offsets"):
        arr.outer_offsets_from_list_of_offsets([])


def test_remove_nan() -> None:
    points0 = np.array([[1.1, 2.2], [3.3, 4.4], [1.1, 2.2]], dtype=point_dtype)
    points1 = np.array([[0, 1], [2, 3], [4, 5], [np.nan, np.nan], [6, 7], [8, 9], [np.nan, np.nan],
                        [-1, -2], [-3, -4], [-5, -6]], dtype=point_dtype)

    points, offsets = arr.remove_nan(points0)
    util_test.assert_point_array(points, allow_nan=False)
    util_test.assert_offset_array(offsets, 3)
    assert_array_almost_equal(points, points0)
    assert_array_equal(offsets, [0, 3])

    points, offsets = arr.remove_nan(points1)
    util_test.assert_point_array(points, allow_nan=True)
    util_test.assert_offset_array(offsets, 8)
    assert_array_almost_equal(
        points, [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [-1, -2], [-3, -4], [-5, -6]],
    )
    assert_array_equal(offsets, [0, 3, 5, 8])


def test_split_codes_by_offsets() -> None:
    codes = np.array([1, 2, 1, 2, 79], dtype=code_dtype)

    list_of_codes = arr.split_codes_by_offsets(codes, np.array([0, 5], dtype=offset_dtype))
    assert isinstance(list_of_codes, list)
    assert len(list_of_codes) == 1
    util_test.assert_code_array(list_of_codes[0], 5)
    assert_array_equal(list_of_codes[0], codes)

    list_of_codes = arr.split_codes_by_offsets(codes, np.array([0, 2, 5], dtype=offset_dtype))
    assert isinstance(list_of_codes, list)
    assert len(list_of_codes) == 2
    util_test.assert_code_array(list_of_codes[0], 2)
    util_test.assert_code_array(list_of_codes[1], 3)
    assert_array_equal(list_of_codes[0], [1, 2])
    assert_array_equal(list_of_codes[1], [1, 2, 79])

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
       arr.split_codes_by_offsets(codes, [0, 5])  # type: ignore[arg-type]

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint32'>"):
        arr.codes_from_offsets(np.array([0, 5], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.codes_from_offsets(np.array([[0, 5]], dtype=offset_dtype))

    with pytest.raises(ValueError, match=r"First element of offset array must be 0"):
        arr.codes_from_offsets(np.array([1, 2], dtype=offset_dtype))


def test_split_points_at_nan() -> None:
    points0 = np.array([[1.1, 2.2], [3.3, 4.4]], dtype=point_dtype)
    points1 = np.array([[0, 1], [2, 3], [np.nan, np.nan], [4, 5], [6, 7], [8, 9], [np.nan, np.nan],
                        [10, 11], [12, 13]], dtype=point_dtype)

    list_of_points = arr.split_points_at_nan(points0)
    assert isinstance(list_of_points, list)
    assert len(list_of_points) == 1
    util_test.assert_point_array(list_of_points[0])
    assert_array_almost_equal(list_of_points[0], points0)

    list_of_points = arr.split_points_at_nan(points1)
    assert isinstance(list_of_points, list)
    assert len(list_of_points) == 3
    for points in list_of_points:
        util_test.assert_point_array(points)
    assert_array_almost_equal(list_of_points[0], [[0, 1], [2, 3]])
    assert_array_almost_equal(list_of_points[1], [[4, 5], [6, 7], [8, 9]])
    assert_array_almost_equal(list_of_points[2], [[10, 11], [12, 13]])

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        arr.split_points_at_nan([[0, 1], [2, 3]])  # type: ignore[arg-type]

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.float64'>"):
        arr.split_points_at_nan(np.array([[0, 1], [2, 3]], dtype=np.float32))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        arr.split_points_at_nan(np.array([[0, 1, 2, 3]], dtype=point_dtype))


def test_split_points_by_offsets() -> None:
    points = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11]], dtype=point_dtype)

    list_of_points = arr.split_points_by_offsets(points, np.array([0, 6], dtype=offset_dtype))
    assert isinstance(list_of_points, list)
    assert len(list_of_points) == 1
    util_test.assert_point_array(list_of_points[0])
    assert_array_almost_equal(list_of_points[0], points)

    list_of_points = arr.split_points_by_offsets(points, np.array([0, 2, 6], dtype=offset_dtype))
    assert isinstance(list_of_points, list)
    assert len(list_of_points) == 2
    util_test.assert_point_array(list_of_points[0])
    util_test.assert_point_array(list_of_points[1])
    assert_array_almost_equal(list_of_points[0], [[0, 1], [2, 3]])
    assert_array_almost_equal(list_of_points[1], [[4, 5], [6, 7], [8, 9], [10, 11]])

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
       arr.split_points_by_offsets(points, [0, 6])  # type: ignore[arg-type]

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint32'>"):
       arr.split_points_by_offsets(points, np.array([0, 6], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
       arr.split_points_by_offsets(points, np.array([[0, 6]], dtype=offset_dtype))

    with pytest.raises(ValueError, match=r"First element of offset array must be 0"):
       arr.split_points_by_offsets(points, np.array([1, 6], dtype=offset_dtype))
