from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest

from contourpy import (
    FillType,
    LineType,
    contour_generator,
    dechunk_filled,
    dechunk_lines,
    dechunk_multi_filled,
    dechunk_multi_lines,
)

from . import util_test

if TYPE_CHECKING:
    import contourpy._contourpy as cpy


@pytest.fixture
def z() -> cpy.CoordinateArray:
    return np.array([[0, 1, 0, 0, 0],
                     [0, 1, 0, 0, 0],
                     [0, 1, 0, 0, 0],
                     [0, 2, 0, 1, 0],
                     [0, 0, 0, 0, 0]], dtype=np.float64)


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
def test_dechunk_filled(z: cpy.CoordinateArray, fill_type: FillType, chunk_size: int) -> None:
    cont_gen = contour_generator(z=z, fill_type=fill_type, chunk_size=chunk_size)
    assert cont_gen.chunk_count == ((2, 2) if chunk_size==2 else (1, 1))
    filled = cont_gen.filled(0.5, 1.5)

    dechunked = dechunk_filled(filled, fill_type)
    util_test.assert_filled(dechunked, fill_type)

    if chunk_size == 0 or fill_type in (FillType.OuterCode, FillType.OuterOffset):
        # Dechunking is a no-op for non-chunked fill types.
        assert dechunked == filled
    else:
        nchunks = len(dechunked[0])
        assert nchunks == 1

        # Note it is important that this contains a polygon with a hole,
        # and using chunk_size=2 there is an empty chunk.
        expected_points = np.array([
            [0.5, 0], [1, 0], [1.5, 0], [1.5, 1], [1.5, 2], [1, 2], [0.5, 2], [0.5, 1], [0.5, 0],
            [0.5, 2], [1, 2], [1.5, 2], [1.75, 3], [1, 3.75], [0.25, 3], [0.5, 2], [1, 2.5],
            [0.75, 3], [1, 3.25], [1.25, 3], [1, 2.5], [2.5, 3], [3, 2.5], [3.5, 3], [3, 3.5],
            [2.5, 3]])
        expected_codes = np.array([1, 2, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79,
                                   1, 2, 2, 2, 79])
        expected_offsets = np.array([0, 9, 16, 21, 26])

        assert dechunked[0][0] is not None
        assert_allclose(dechunked[0][0], expected_points)

        if fill_type == FillType.ChunkCombinedCode:
            if TYPE_CHECKING:
                dechunked = cast(cpy.FillReturn_ChunkCombinedCode, dechunked)
            assert dechunked[1][0] is not None
            assert_array_equal(dechunked[1][0], expected_codes)
        elif fill_type == FillType.ChunkCombinedOffset:
            if TYPE_CHECKING:
                dechunked = cast(cpy.FillReturn_ChunkCombinedOffset, dechunked)
            assert dechunked[1][0] is not None
            assert_array_equal(dechunked[1][0], expected_offsets)
        elif fill_type == FillType.ChunkCombinedCodeOffset:
            if TYPE_CHECKING:
                dechunked = cast(cpy.FillReturn_ChunkCombinedCodeOffset, dechunked)
            assert dechunked[1][0] is not None
            assert_array_equal(dechunked[1][0], expected_codes)
            assert dechunked[2][0] is not None
            assert_array_equal(dechunked[2][0], [0, 9, 21, 26])
        elif fill_type == FillType.ChunkCombinedOffsetOffset:
            if TYPE_CHECKING:
                dechunked = cast(cpy.FillReturn_ChunkCombinedOffsetOffset, dechunked)
            assert dechunked[1][0] is not None
            assert_array_equal(dechunked[1][0], expected_offsets)
            assert dechunked[2][0] is not None
            assert_array_equal(dechunked[2][0], [0, 1, 3, 4])
        else:
            raise RuntimeError(f"Unexpected fill_type {fill_type}")


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 1))
def test_dechunk_filled_empty(z: cpy.CoordinateArray, fill_type: FillType, chunk_size: int) -> None:
    cont_gen = contour_generator(z=z, fill_type=fill_type, chunk_size=chunk_size)
    filled = cont_gen.filled(3, 4)

    dechunked = dechunk_filled(filled, fill_type)
    util_test.assert_filled(dechunked, fill_type)

    if fill_type in (FillType.OuterCode, FillType.OuterOffset):
        assert dechunked == ([], [])
    elif fill_type in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset):
        assert dechunked == ([None], [None])
    elif fill_type in (FillType.ChunkCombinedCodeOffset, FillType.ChunkCombinedOffsetOffset):
        assert dechunked == ([None], [None], [None])
    else:
        raise RuntimeError(f"Unexpected fill_type {fill_type}")


@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
def test_dechunk_lines(z: cpy.CoordinateArray, line_type: LineType, chunk_size: int) -> None:
    cont_gen = contour_generator(z=z, line_type=line_type, chunk_size=chunk_size)
    assert cont_gen.chunk_count == ((2, 2) if chunk_size==2 else (1, 1))
    lines = cont_gen.lines(0.5)

    dechunked = dechunk_lines(lines, line_type)
    util_test.assert_lines(dechunked, line_type)

    if chunk_size == 0 or line_type in (LineType.Separate, LineType.SeparateCode):
        # Dechunking is a no-op for non-chunked line types.
        assert dechunked == lines
    else:
        nchunks = len(dechunked[0])
        assert nchunks == 1

        # Note it is important that this contains a closed line loop as well as open line strips,
        # and using chunk_size=2 there is an empty chunk.
        expected_points = np.array([
            [1.5, 0], [1.5, 1], [1.5, 2], [0.5, 2], [0.5, 1], [0.5, 0], [1.5, 2], [1.75, 3],
            [1, 3.75], [0.25, 3], [0.5, 2], [2.5, 3], [3, 2.5], [3.5, 3], [3, 3.5], [2.5, 3]])
        expected_codes = np.array([1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 79])
        expected_offsets = np.array([0, 3, 6, 11, 16])

        if line_type == LineType.ChunkCombinedCode:
            if TYPE_CHECKING:
                dechunked = cast(cpy.LineReturn_ChunkCombinedCode, dechunked)
            assert dechunked[0][0] is not None
            assert_allclose(dechunked[0][0], expected_points)
            assert dechunked[1][0] is not None
            assert_array_equal(dechunked[1][0], expected_codes)
        elif line_type == LineType.ChunkCombinedOffset:
            if TYPE_CHECKING:
                dechunked = cast(cpy.LineReturn_ChunkCombinedOffset, dechunked)
            assert dechunked[0][0] is not None
            assert_allclose(dechunked[0][0], expected_points)
            assert dechunked[1][0] is not None
            assert_array_equal(dechunked[1][0], expected_offsets)
        elif line_type == LineType.ChunkCombinedNan:
            if TYPE_CHECKING:
                dechunked = cast(cpy.LineReturn_ChunkCombinedNan, dechunked)
            assert dechunked[0][0] is not None
            # Convert offsets to int64 to avoid numpy error when mixing signed and unsigned ints.
            expected = np.insert(expected_points, expected_offsets[1:-1].astype(np.int64),
                                 [np.nan, np.nan], axis=0)
            assert_allclose(dechunked[0][0], expected)
        else:
            raise RuntimeError(f"Unexpected line_type {line_type}")


@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 1))
def test_dechunk_lines_empty(z: cpy.CoordinateArray, line_type: LineType, chunk_size: int) -> None:
    cont_gen = contour_generator(z=z, line_type=line_type, chunk_size=chunk_size)
    lines = cont_gen.lines(4)

    dechunked = dechunk_lines(lines, line_type)
    util_test.assert_lines(dechunked, line_type)

    if line_type == LineType.Separate:
        assert dechunked == []
    elif line_type == LineType.SeparateCode:
        assert dechunked == ([], [])
    elif line_type in (LineType.ChunkCombinedCode, LineType.ChunkCombinedOffset):
        assert dechunked == ([None], [None])
    elif line_type == LineType.ChunkCombinedNan:
        assert dechunked == ([None],)
    else:
        raise RuntimeError(f"Unexpected line_type {line_type}")


@pytest.mark.parametrize("fill_type", FillType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
def test_dechunk_multi_filled(z: cpy.CoordinateArray, fill_type: FillType, chunk_size: int) -> None:
    cont_gen = contour_generator(z=z, fill_type=fill_type, chunk_size=chunk_size)
    assert cont_gen.chunk_count == ((2, 2) if chunk_size==2 else (1, 1))
    levels = [0.5, 1.5, 2.5]
    multi_filled = cont_gen.multi_filled(levels)

    multi_dechunked = dechunk_multi_filled(multi_filled, fill_type)
    individual_dechunked = [dechunk_filled(filled, fill_type) for filled in multi_filled]

    assert isinstance(multi_dechunked, list)
    assert isinstance(individual_dechunked, list)
    assert len(multi_dechunked) == len(levels) - 1
    assert len(individual_dechunked) == len(levels) - 1

    for from_multi, from_individual in zip(multi_dechunked, individual_dechunked):
        util_test.assert_filled(from_multi, fill_type)
        util_test.assert_filled(from_individual, fill_type)
        util_test.assert_equal_recursive(from_multi, from_individual)


@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
def test_dechunk_multi_lines(z: cpy.CoordinateArray, line_type: LineType, chunk_size: int) -> None:
    cont_gen = contour_generator(z=z, line_type=line_type, chunk_size=chunk_size)
    assert cont_gen.chunk_count == ((2, 2) if chunk_size==2 else (1, 1))
    levels = [-0.5, 0.5, 1.5]
    multi_lines = cont_gen.multi_lines(levels)

    multi_dechunked = dechunk_multi_lines(multi_lines, line_type)
    individual_dechunked = [dechunk_lines(lines, line_type) for lines in multi_lines]

    assert isinstance(multi_dechunked, list)
    assert isinstance(individual_dechunked, list)
    assert len(multi_dechunked) == len(levels)
    assert len(individual_dechunked) == len(levels)

    for from_multi, from_individual in zip(multi_dechunked, individual_dechunked):
        util_test.assert_lines(from_multi, line_type)
        util_test.assert_lines(from_individual, line_type)
        util_test.assert_equal_recursive(from_multi, from_individual)
