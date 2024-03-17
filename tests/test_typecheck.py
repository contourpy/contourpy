from __future__ import annotations

import numpy as np
import pytest

from contourpy import FillType, LineType
from contourpy.typecheck import (
    check_code_array,
    check_filled,
    check_lines,
    check_offset_array,
    check_point_array,
)
from contourpy.types import code_dtype, offset_dtype, point_dtype


def test_check_code_array() -> None:
    # Valid code array, does not raise.
    check_code_array(np.array([1, 2, 79], dtype=code_dtype))

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_code_array([1, 2, 79])

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint8'>"):
        check_code_array(np.array([1, 2, 79], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        check_code_array(np.array([[1, 2, 79]], dtype=code_dtype))

    with pytest.raises(ValueError, match=r"First element of code array must be 1"):
        check_code_array(np.array([2, 2, 79], dtype=code_dtype))


def test_check_offset_array() -> None:
    # Valid offset array, does not raise.
    check_offset_array(np.array([0, 5], dtype=offset_dtype))

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_offset_array([0, 5])

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint32'>"):
        check_offset_array(np.array([0, 5], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        check_offset_array(np.array([[0], [5]], dtype=offset_dtype))

    with pytest.raises(ValueError, match=r"First element of offset array must be 0"):
        check_offset_array(np.array([1, 5], dtype=offset_dtype))


def test_check_point_array() -> None:
    # Valid point array, does not raise.
    check_point_array(np.array([[1.1, 2.2], [3.3, 4.4]], dtype=point_dtype))

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_point_array([[1.1, 2.2], [3.3, 4.4]])

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.float64'>"):
        check_point_array(np.array([[1.1, 2.2], [3.3, 4.4]], dtype=np.float32))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        check_point_array(np.array([[1.1, 2.2, 3.3, 4.4]], dtype=point_dtype))


def test_check_filled_OuterCode() -> None:
    # Valid filled, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]], dtype=point_dtype)
    codes = np.array([1, 2, 79], dtype=code_dtype)
    check_filled(([points], [codes]), FillType.OuterCode)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_filled([], FillType.OuterCode)
    with pytest.raises(ValueError, match=r"Expected tuple of length 2 not 3"):
        check_filled(([], [], []), FillType.OuterCode)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 2 lists"):
        check_filled(([], None), FillType.OuterCode)
    with pytest.raises(ValueError, match=r"Expected 2 lists with same length"):
        check_filled(([1, 2, 3], [1, 2]), FillType.OuterCode)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([list(points)], [codes]), FillType.OuterCode)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [list(codes)]), FillType.OuterCode)

    with pytest.raises(ValueError, match=r"Points and codes have different lengths in polygon 0"):
        check_filled(([points], [codes[:-1]]), FillType.OuterCode)


def test_check_filled_OuterOffset() -> None:
    # Valid filled, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8]], dtype=point_dtype)
    offsets = np.array([0, 2, 4], dtype=offset_dtype)
    check_filled(([points], [offsets]), FillType.OuterOffset)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_filled([], FillType.OuterOffset)
    with pytest.raises(ValueError, match=r"Expected tuple of length 2 not 3"):
        check_filled(([], [], []), FillType.OuterOffset)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 2 lists"):
        check_filled(([], None), FillType.OuterOffset)
    with pytest.raises(ValueError, match=r"Expected 2 lists with same length"):
        check_filled(([1, 2, 3], [1, 2]), FillType.OuterOffset)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([list(points)], [offsets]), FillType.OuterOffset)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [list(offsets)]), FillType.OuterOffset)

    with pytest.raises(ValueError, match=r"Inconsistent points and offsets in polygon 0"):
        check_filled(([points], [offsets[:-1]]), FillType.OuterOffset)


def test_check_filled_ChunkCombinedCode() -> None:
    # Valid filled, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]], dtype=point_dtype)
    codes = np.array([1, 2, 79], dtype=code_dtype)
    check_filled(([points], [codes]), FillType.ChunkCombinedCode)
    check_filled(([None], [None]), FillType.ChunkCombinedCode)
    check_filled(([None, points], [None, codes]), FillType.ChunkCombinedCode)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_filled([], FillType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Expected tuple of length 2 not 3"):
        check_filled(([], [], []), FillType.ChunkCombinedCode)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 2 lists"):
        check_filled(([], None), FillType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Expected 2 lists with same length"):
        check_filled(([1, 2, 3], [1, 2]), FillType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Expected 2 non-empty lists"):
        check_filled(([], []), FillType.ChunkCombinedCode)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([list(points)], [codes]), FillType.ChunkCombinedCode)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [list(codes)]), FillType.ChunkCombinedCode)

    with pytest.raises(ValueError, match=r"Points and codes have different lengths in chunk 1"):
        check_filled(([None, points], [None, codes[:-1]]), FillType.ChunkCombinedCode)

    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([points], [None]), FillType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([None], [codes]), FillType.ChunkCombinedCode)


def test_check_filled_ChunkCombinedOffset() -> None:
    # Valid filled, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8]], dtype=point_dtype)
    offsets = np.array([0, 2, 4], dtype=offset_dtype)
    check_filled(([points], [offsets]), FillType.ChunkCombinedOffset)
    check_filled(([None], [None]), FillType.ChunkCombinedOffset)
    check_filled(([None, points], [None, offsets]), FillType.ChunkCombinedOffset)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_filled([], FillType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Expected tuple of length 2 not 3"):
        check_filled(([], [], []), FillType.ChunkCombinedOffset)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 2 lists"):
        check_filled(([], None), FillType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Expected 2 lists with same length"):
        check_filled(([1, 2, 3], [1, 2]), FillType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Expected 2 non-empty lists"):
        check_filled(([], []), FillType.ChunkCombinedOffset)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([list(points)], [offsets]), FillType.ChunkCombinedOffset)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [list(offsets)]), FillType.ChunkCombinedOffset)

    with pytest.raises(ValueError, match=r"Inconsistent points and offsets in chunk 1"):
        check_filled(([None, points], [None, offsets[:-1]]), FillType.ChunkCombinedOffset)

    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([points], [None]), FillType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([None], [offsets]), FillType.ChunkCombinedOffset)


def test_check_filled_ChunkCombinedCodeOffset() -> None:
    # Valid filled, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8]], dtype=point_dtype)
    codes = np.array([1, 2, 1, 79], dtype=code_dtype)
    outer_offsets = np.array([0, 4], dtype=offset_dtype)
    check_filled(([points], [codes], [outer_offsets]), FillType.ChunkCombinedCodeOffset)
    check_filled(([None], [None], [None]), FillType.ChunkCombinedCodeOffset)
    check_filled(([None, points], [None, codes], [None, outer_offsets]),
                 FillType.ChunkCombinedCodeOffset)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_filled([], FillType.ChunkCombinedCodeOffset)
    with pytest.raises(ValueError, match=r"Expected tuple of length 3 not 2"):
        check_filled(([], []), FillType.ChunkCombinedCodeOffset)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 3 lists"):
        check_filled(([], None, []), FillType.ChunkCombinedCodeOffset)
    with pytest.raises(ValueError, match=r"Expected 3 lists with same length"):
        check_filled(([1, 2, 3], [1, 2], [1, 2, 3]), FillType.ChunkCombinedCodeOffset)
    with pytest.raises(ValueError, match=r"Expected 3 non-empty lists"):
        check_filled(([], [], []), FillType.ChunkCombinedCodeOffset)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([list(points)], [codes], [outer_offsets]), FillType.ChunkCombinedCodeOffset)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [list(codes)], [outer_offsets]), FillType.ChunkCombinedCodeOffset)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [codes], [list(outer_offsets)]), FillType.ChunkCombinedCodeOffset)

    with pytest.raises(ValueError, match=r"Points and codes have different lengths in chunk 1"):
        check_filled(([None, points], [None, codes[:-1]], [None, outer_offsets]),
                     FillType.ChunkCombinedCodeOffset)
    with pytest.raises(ValueError, match=r"Inconsistent codes and outer_offsets in chunk 0"):
        check_filled(([points], [codes], [np.array([0, 4, 5], dtype=offset_dtype)]),
                     FillType.ChunkCombinedCodeOffset)

    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([points], [codes], [None]), FillType.ChunkCombinedCodeOffset)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([points], [None], [outer_offsets]), FillType.ChunkCombinedCodeOffset)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([None], [codes], [outer_offsets]), FillType.ChunkCombinedCodeOffset)


def test_check_filled_ChunkCombinedOffsetOffset() -> None:
    # Valid filled, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8]], dtype=point_dtype)
    offsets = np.array([0, 2, 4], dtype=offset_dtype)
    outer_offsets = np.array([0, 2], dtype=offset_dtype)
    check_filled(([points], [offsets], [outer_offsets]), FillType.ChunkCombinedOffsetOffset)
    check_filled(([None], [None], [None]), FillType.ChunkCombinedOffsetOffset)
    check_filled(([None, points], [None, offsets], [None, outer_offsets]),
                 FillType.ChunkCombinedOffsetOffset)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_filled([], FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(ValueError, match=r"Expected tuple of length 3 not 2"):
        check_filled(([], []), FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 3 lists"):
        check_filled(([], None, []), FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(ValueError, match=r"Expected 3 lists with same length"):
        check_filled(([1, 2, 3], [1, 2], [1, 2, 3]), FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(ValueError, match=r"Expected 3 non-empty lists"):
        check_filled(([], [], []), FillType.ChunkCombinedOffsetOffset)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([list(points)], [offsets], [outer_offsets]),
                      FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [list(offsets)], [outer_offsets]),
                      FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_filled(([points], [offsets], [list(outer_offsets)]),
                      FillType.ChunkCombinedOffsetOffset)

    with pytest.raises(ValueError, match=r"Inconsistent points and offsets in chunk 1"):
        check_filled(([None, points], [None, offsets[:-1]], [None, outer_offsets]),
                     FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(ValueError, match=r"Inconsistent offsets and outer_offsets in chunk 0"):
        check_filled(([points], [offsets], [np.array([0, 4, 5], dtype=offset_dtype)]),
                     FillType.ChunkCombinedOffsetOffset)

    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([points], [offsets], [None]), FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([points], [None], [outer_offsets]), FillType.ChunkCombinedOffsetOffset)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_filled(([None], [offsets], [outer_offsets]), FillType.ChunkCombinedOffsetOffset)


def test_check_lines_Separate() -> None:
    # Valid lines, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4]], dtype=point_dtype)
    check_lines([points], LineType.Separate)

    with pytest.raises(TypeError, match=r"Expected list not <class 'tuple'>"):
        check_lines((), LineType.Separate)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_lines([[]], LineType.Separate)


def test_check_lines_SeparateCode() -> None:
    # Valid lines, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]], dtype=point_dtype)
    codes = np.array([1, 2, 79], dtype=code_dtype)
    check_lines(([points], [codes]), LineType.SeparateCode)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_lines([], LineType.SeparateCode)
    with pytest.raises(ValueError, match=r"Expected tuple of length 2 not 3"):
        check_lines(([], [], []), LineType.SeparateCode)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 2 lists"):
        check_lines(([], None), LineType.SeparateCode)
    with pytest.raises(ValueError, match=r"Expected 2 lists with same length"):
        check_lines(([1, 2, 3], [1, 2]), LineType.SeparateCode)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_lines(([list(points)], [codes]), LineType.SeparateCode)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'"):
        check_lines(([points], [list(codes)]), LineType.SeparateCode)

    with pytest.raises(ValueError, match=r"Points and codes have different lengths in line 0"):
        check_lines(([points], [codes[:-1]]), LineType.SeparateCode)


def test_check_lines_ChunkCombinedCode() -> None:
    # Valid lines, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8]], dtype=point_dtype)
    codes = np.array([1, 2, 1, 2], dtype=code_dtype)
    check_lines(([points], [codes]), LineType.ChunkCombinedCode)
    check_lines(([None], [None]), LineType.ChunkCombinedCode)
    check_lines(([None, points], [None, codes]), LineType.ChunkCombinedCode)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_lines([], LineType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Expected tuple of length 2 not 3"):
        check_lines(([], [], []), LineType.ChunkCombinedCode)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 2 lists"):
        check_lines(([], None), LineType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Expected 2 lists with same length"):
        check_lines(([None, None], [None]), LineType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Expected 2 non-empty lists"):
        check_lines(([], []), LineType.ChunkCombinedCode)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_lines(([list(points)], [codes]), LineType.ChunkCombinedCode)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_lines(([points], [list(codes)]), LineType.ChunkCombinedCode)

    with pytest.raises(ValueError, match=r"Points and codes have different lengths in chunk 1"):
        check_lines(([None, points], [None, codes[:-1]]), LineType.ChunkCombinedCode)

    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_lines(([points], [None]), LineType.ChunkCombinedCode)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_lines(([None], [codes]), LineType.ChunkCombinedCode)


def test_check_lines_ChunkCombinedOffset() -> None:
    # Valid lines, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6], [7.7, 8.8]], dtype=point_dtype)
    offsets = np.array([0, 2, 4], dtype=offset_dtype)
    check_lines(([points], [offsets]), LineType.ChunkCombinedOffset)
    check_lines(([None], [None]), LineType.ChunkCombinedOffset)
    check_lines(([None, points], [None, offsets]), LineType.ChunkCombinedOffset)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_lines([], LineType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Expected tuple of length 2 not 3"):
        check_lines(([], [], []), LineType.ChunkCombinedOffset)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 2 lists"):
        check_lines(([], None), LineType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Expected 2 lists with same length"):
        check_lines(([None, None], [None]), LineType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Expected 2 non-empty lists"):
        check_lines(([], []), LineType.ChunkCombinedOffset)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_lines(([list(points)], [offsets]), LineType.ChunkCombinedOffset)
    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_lines(([points], [list(offsets)]), LineType.ChunkCombinedOffset)

    with pytest.raises(ValueError, match=r"Inconsistent points and offsets in chunk 1"):
        check_lines(([None, points], [None, offsets[:-1]]), LineType.ChunkCombinedOffset)

    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_lines(([points], [None]), LineType.ChunkCombinedOffset)
    with pytest.raises(ValueError, match=r"Inconsistent Nones in chunk 0"):
        check_lines(([None], [offsets]), LineType.ChunkCombinedOffset)


def test_check_lines_ChunkCombinedNan() -> None:
    # Valid lines, does not raise.
    points = np.array([[1.1, 2.2], [3.3, 4.4], [np.nan, np.nan], [5.5, 6.6], [7.7, 8.8]],
                       dtype=point_dtype)
    check_lines(([points],), LineType.ChunkCombinedNan)
    check_lines(([None],), LineType.ChunkCombinedNan)
    check_lines(([None, points],), LineType.ChunkCombinedNan)

    with pytest.raises(TypeError, match=r"Expected tuple not <class 'list'>"):
        check_lines([], LineType.ChunkCombinedNan)
    with pytest.raises(ValueError, match=r"Expected tuple of length 1 not 2"):
        check_lines(([], []), LineType.ChunkCombinedNan)
    with pytest.raises(TypeError, match=r"Expected tuple to contain 1 lists"):
        check_lines((None,), LineType.ChunkCombinedNan)
    with pytest.raises(ValueError, match=r"Expected 1 non-empty lists"):
        check_lines(([],), LineType.ChunkCombinedNan)

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_lines(([list(points)],), LineType.ChunkCombinedNan)
