# Minimal set of tests to check the returns from all algorithms and line/fill types.
# If only one test file is run then this is the one.
# Based on the examples in the docs for line_type and fill_type.
# Tests are chunked as that is the only way to test the threaded algorithm.

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
import pytest

from contourpy import FillType, LineType, contour_generator

from . import util_test

if TYPE_CHECKING:
    import contourpy._contourpy as cpy


@pytest.fixture
def z() -> cpy.PointArray:
    return np.array([
        [1.4, 1.2, 0.9, 0.0],
        [0.6, 3.0, 0.4, 0.7],
        [0.2, 0.2, 0.5, 3.0],
    ])


@pytest.mark.parametrize("name,line_type", util_test.all_names_and_line_types())
def test_minimal_lines(name: str, line_type: LineType, z: cpy.PointArray) -> None:
    cont_gen = contour_generator(z=z, name=name, line_type=line_type, chunk_count=(1, 2))
    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 2)
    assert cont_gen.chunk_size == (2, 2)

    assert cont_gen.thread_count < 10

    lines = cont_gen.lines(2)
    util_test.assert_lines(lines, line_type)

    # Expected values by chunk.
    expected_points: list[cpy.PointArray] = [
        np.array([[0.58333333, 1.0], [1.0, 0.44444444], [1.38461538, 1.0], [1.0, 1.35714286],
                  [0.58333333, 1.0]]),
        np.array([[2.6, 2.0], [3.0, 1.56521739]]),
    ]
    expected_codes: list[cpy.CodeArray] = [
        np.array([1, 2, 2, 2, 79], dtype=np.uint8),
        np.array([1, 2], dtype=np.uint8),
    ]
    expected_offsets: list[cpy.OffsetArray] = [
        np.array([0, 5], dtype=np.uint32),
        np.array([0, 2], dtype=np.uint32),
    ]

    # Order of returned lines/points different for mpl2005/2014 algorithms.
    if name == "mpl2005":
        expected_points[0] = np.vstack((expected_points[0][1:], expected_points[0][1]))
        expected_points[1] = expected_points[1][::-1]
    elif name == "mpl2014":
        expected_points = expected_points[::-1]
        expected_points[1] = np.vstack((expected_points[1][1:], expected_points[1][1]))
        expected_codes = expected_codes[::-1]

    if line_type == LineType.Separate:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_Separate, lines)
        if cont_gen.thread_count > 1 and len(lines[0]) == 2:
            # Threaded algorithm can return lines in any order.
            expected_points = expected_points[::-1]
        util_test.assert_equal_recursive(lines, expected_points)
    elif line_type == LineType.SeparateCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_SeparateCode, lines)
        if cont_gen.thread_count > 1 and len(lines[0][0]) == 2:
            # Threaded algorithm can return lines in any order.
            expected_points = expected_points[::-1]
            expected_codes = expected_codes[::-1]
        util_test.assert_equal_recursive(lines, (expected_points, expected_codes))
    elif line_type == LineType.ChunkCombinedCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedCode, lines)
        util_test.assert_equal_recursive(lines, (expected_points, expected_codes))
    elif line_type == LineType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedOffset, lines)
        util_test.assert_equal_recursive(lines, (expected_points, expected_offsets))
    elif line_type == LineType.ChunkCombinedNan:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedNan, lines)
        util_test.assert_equal_recursive(lines, (expected_points,))
    else:
        raise RuntimeError(f"Unexpected line_type {line_type}")


@pytest.mark.parametrize("name,fill_type", util_test.all_names_and_fill_types())
def test_minimal_filled(name: str, fill_type: FillType, z: cpy.PointArray) -> None:
    cont_gen = contour_generator(z=z, name=name, fill_type=fill_type, chunk_count=(1, 2))
    assert cont_gen.fill_type == fill_type
    assert cont_gen.chunk_count == (1, 2)
    assert cont_gen.chunk_size == (2, 2)

    filled = cont_gen.filled(1, 2)
    util_test.assert_filled(filled, fill_type)

    # Expected values by chunk.
    expected_points: list[cpy.PointArray] = [
        np.array([[0.0, 0.0], [1.0, 0.0], [1.66666667, 0.0], [1.76923077, 1.0], [1.0, 1.71428571],
                  [0.16666667, 1.0], [0.0, 0.5], [0.0, 0.0], [1.0, 0.44444444], [0.58333333, 1.0],
                  [1.0, 1.35714286], [1.38461538, 1.0], [1.0, 0.44444444]]),
        np.array([[2.2, 2.0], [3.0, 1.13043478], [3.0, 1.56521739], [2.6, 2.0], [2.2, 2.0]]),
    ]
    expected_codes: list[cpy.CodeArray] = [
        np.array([1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79], dtype=np.uint8),
        np.array([1, 2, 2, 2, 79], dtype=np.uint8),
    ]
    expected_offsets: list[cpy.OffsetArray] = [
        np.array([0, 8, 13], dtype=np.uint32),
        np.array([0, 5], dtype=np.uint32),
    ]
    expected_outer_offsets: list[cpy.OffsetArray] = [
        np.array([0, 13], dtype=np.uint32),
        np.array([0, 5], dtype=np.uint32),
    ]
    expected_outer_offsets2: list[cpy.OffsetArray] = [
        np.array([0, 2], dtype=np.uint32),
        np.array([0, 1], dtype=np.uint32),
    ]

     # Order of returned lines/points different for mpl2005/2014 algorithms.
    if name == "mpl2014":
        outer = expected_points[0][:8]
        hole = expected_points[0][8:]
        outer = np.vstack((outer[1:], outer[1]))
        hole = np.vstack((hole[1:], hole[1]))
        expected_points[0] = np.vstack((outer, hole))
    if name in ("mpl2005", "mpl2014"):
        expected_points[1] = np.vstack((expected_points[1][1:], expected_points[1][1]))

    if fill_type == FillType.OuterCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterCode, filled)
        if cont_gen.thread_count > 1 and len(filled[0][0]) == 5:
            # Threaded algorithm can return lines in any order.
            expected_points = expected_points[::-1]
            expected_codes = expected_codes[::-1]
        util_test.assert_equal_recursive(filled, (expected_points, expected_codes))
    elif fill_type == FillType.OuterOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterOffset, filled)
        if cont_gen.thread_count > 1 and len(filled[0][0]) == 5:
            # Threaded algorithm can return lines in any order.
            expected_points = expected_points[::-1]
            expected_offsets = expected_offsets[::-1]
        util_test.assert_equal_recursive(filled, (expected_points, expected_offsets))
    elif fill_type == FillType.ChunkCombinedCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCode, filled)
        util_test.assert_equal_recursive(filled, (expected_points, expected_codes))
    elif fill_type == FillType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffset, filled)
        util_test.assert_equal_recursive(filled, (expected_points, expected_offsets))
    elif fill_type == FillType.ChunkCombinedCodeOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCodeOffset, filled)
        util_test.assert_equal_recursive(
            filled,
            (expected_points, expected_codes, expected_outer_offsets),
        )
    elif fill_type == FillType.ChunkCombinedOffsetOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffsetOffset, filled)
        util_test.assert_equal_recursive(
            filled,
            (expected_points, expected_offsets, expected_outer_offsets2),
        )
    else:
        raise RuntimeError(f"Unexpected fill_type {fill_type}")
