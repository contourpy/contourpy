from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

from contourpy import LineType, contour_generator, convert_line_type, dechunk_lines

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


@pytest.mark.parametrize("line_type_from", LineType.__members__.values())
@pytest.mark.parametrize("line_type_to", LineType.__members__.values())
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
