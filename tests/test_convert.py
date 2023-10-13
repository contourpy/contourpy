from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

from contourpy import (
    FillType, LineType, contour_generator, convert_fill_type, convert_line_type, dechunk_filled,
    dechunk_lines,
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


@pytest.mark.parametrize("fill_type_to", FillType.__members__.values())
@pytest.mark.parametrize("fill_type_from", FillType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
@pytest.mark.parametrize("empty", (False, True))
def test_convert_fill_type(
    z: cpy.CoordinateArray,
    fill_type_from: FillType,
    fill_type_to: FillType,
    chunk_size: int,
    empty: bool,
) -> None:
    if empty:
        # Levels outside of z bounds so no polygons produced.
        lower_level, upper_level = 3.0, 4.0
    else:
        # Using chunk_size=2 there is an empty chunk.
        lower_level, upper_level = 0.5, 1.5

    filled = contour_generator(z=z, fill_type=fill_type_from, chunk_size=chunk_size).filled(
        lower_level, upper_level)

    if (fill_type_from in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset) and
        fill_type_to not in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset)):
        msg = f"Conversion from {fill_type_from} to {fill_type_to} not supported"
        with pytest.raises(ValueError, match=msg):
            convert_fill_type(filled, fill_type_from, fill_type_to)
    else:
        converted = convert_fill_type(filled, fill_type_from, fill_type_to)

        compare = contour_generator(z=z, fill_type=fill_type_to, chunk_size=chunk_size).filled(
            lower_level, upper_level)

        # Converting OuterCode or OuterOffset to any ChunkCombined* returns all polygons in a single
        # chunk, so need to compare to dechunked_filled(compare).
        if (fill_type_from in (FillType.OuterCode, FillType.OuterOffset) and
            fill_type_to not in (FillType.OuterCode, FillType.OuterOffset)):
            compare = dechunk_filled(compare, fill_type_to)

            util_test.assert_equal_recursive(converted, compare)


@pytest.mark.parametrize("line_type_to", LineType.__members__.values())
@pytest.mark.parametrize("line_type_from", LineType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
@pytest.mark.parametrize("empty", (False, True))
def test_convert_line_type(
    z: cpy.CoordinateArray,
    line_type_from: LineType,
    line_type_to: LineType,
    chunk_size: int,
    empty: bool,
) -> None:
    if empty:
        # Level outside of z bounds so no lines produced.
        level = 4.0
    else:
        # Lines includes a closed line loop as well as open line strips,
        # and using chunk_size=2 there is an empty chunk.
        level = 0.5
    lines = contour_generator(z=z, line_type=line_type_from, chunk_size=chunk_size).lines(level)
    converted = convert_line_type(lines, line_type_from, line_type_to)

    compare = contour_generator(z=z, line_type=line_type_to, chunk_size=chunk_size).lines(level)

    # Converting Separate or SeparateCode to any ChunkCombined* returns all lines in a single chunk,
    # so need to compare to dechunked_lines(compare).
    if (line_type_from in (LineType.Separate, LineType.SeparateCode) and
        line_type_to not in (LineType.Separate, LineType.SeparateCode)):
       compare = dechunk_lines(compare, line_type_to)

    util_test.assert_equal_recursive(converted, compare)
