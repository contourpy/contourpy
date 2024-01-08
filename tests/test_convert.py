from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

from contourpy import (
    FillType,
    LineType,
    contour_generator,
    convert_filled,
    convert_lines,
    convert_multi_filled,
    convert_multi_lines,
    dechunk_filled,
    dechunk_lines,
)

from . import util_test

if TYPE_CHECKING:
    import contourpy._contourpy as cpy


@pytest.fixture
def z() -> cpy.CoordinateArray:
    # Care needed with test data as although arbitrary z produces identical results for lines
    # regardless of line_type, this is not the case for filled as the order that polygons are
    # produced is different depending on whether the relationship between outer and inner
    # boundaries is calculated. If it is then inner boundaries directly follow their outer boundary,
    # if not then the boundaries are returned in the order they are found.
    # This test data is chosen so that filled results are always the same.
    return np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 2, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1],
    ], dtype=np.float64)


@pytest.mark.parametrize("fill_type_to", FillType.__members__.values())
@pytest.mark.parametrize("fill_type_from", FillType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2, 3))
@pytest.mark.parametrize("empty", (False, True))
def test_convert_filled(
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
        # Using chunk_size=2 or 3 there is an empty chunk.
        lower_level, upper_level = 0.5, 1.5

    filled = contour_generator(z=z, fill_type=fill_type_from, chunk_size=chunk_size).filled(
        lower_level, upper_level)

    if (fill_type_from in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset) and
        fill_type_to not in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset)):
        msg = f"Conversion from {fill_type_from} to {fill_type_to} not supported"
        with pytest.raises(ValueError, match=msg):
            convert_filled(filled, fill_type_from, fill_type_to)
    else:
        converted = convert_filled(filled, fill_type_from, fill_type_to)
        util_test.assert_filled(converted, fill_type_to)

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
@pytest.mark.parametrize("chunk_size", (0, 2, 3))
@pytest.mark.parametrize("empty", (False, True))
def test_convert_lines(
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
        # and using chunk_size=2 or 3 there is an empty chunk.
        level = 0.5
    lines = contour_generator(z=z, line_type=line_type_from, chunk_size=chunk_size).lines(level)
    converted = convert_lines(lines, line_type_from, line_type_to)

    compare = contour_generator(z=z, line_type=line_type_to, chunk_size=chunk_size).lines(level)
    util_test.assert_lines(converted, line_type_to)

    # Converting Separate or SeparateCode to any ChunkCombined* returns all lines in a single chunk,
    # so need to compare to dechunked_lines(compare).
    if (line_type_from in (LineType.Separate, LineType.SeparateCode) and
        line_type_to not in (LineType.Separate, LineType.SeparateCode)):
       compare = dechunk_lines(compare, line_type_to)

    util_test.assert_equal_recursive(converted, compare)


@pytest.mark.parametrize("fill_type_to", FillType.__members__.values())
@pytest.mark.parametrize("fill_type_from", FillType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
def test_convert_multi_filled(
    z: cpy.CoordinateArray,
    fill_type_from: FillType,
    fill_type_to: FillType,
    chunk_size: int,
) -> None:
    levels = [0.5, 1.5, 2.5]
    cont_gen = contour_generator(z=z, fill_type=fill_type_from, chunk_size=chunk_size)
    multi_filled = cont_gen.multi_filled(levels)

    if (fill_type_from in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset) and
        fill_type_to not in (FillType.ChunkCombinedCode, FillType.ChunkCombinedOffset)):
        msg = f"Conversion from {fill_type_from} to {fill_type_to} not supported"
        with pytest.raises(ValueError, match=msg):
            convert_multi_filled(multi_filled, fill_type_from, fill_type_to)
    else:
        multi_converted = convert_multi_filled(multi_filled, fill_type_from, fill_type_to)
        individual_converted = [convert_filled(filled, fill_type_from, fill_type_to)
                                for filled in multi_filled]

        assert isinstance(multi_converted, list)
        assert isinstance(individual_converted, list)
        assert len(multi_converted) == len(levels) - 1
        assert len(individual_converted) == len(levels) - 1

        for from_multi, from_individual in zip(multi_converted, individual_converted):
            util_test.assert_filled(from_multi, fill_type_to)
            util_test.assert_filled(from_individual, fill_type_to)
            util_test.assert_equal_recursive(from_multi, from_individual)


@pytest.mark.parametrize("line_type_to", LineType.__members__.values())
@pytest.mark.parametrize("line_type_from", LineType.__members__.values())
@pytest.mark.parametrize("chunk_size", (0, 2))
def test_convert_multi_lines(
    z: cpy.CoordinateArray,
    line_type_from: LineType,
    line_type_to: LineType,
    chunk_size: int,
) -> None:
    levels = [-0.5, 0.5, 1.5]
    cont_gen = contour_generator(z=z, line_type=line_type_from, chunk_size=chunk_size)
    multi_lines = cont_gen.multi_lines(levels)

    multi_converted = convert_multi_lines(multi_lines, line_type_from, line_type_to)
    individual_converted = [convert_lines(lines, line_type_from, line_type_to)
                            for lines in multi_lines]

    assert isinstance(multi_converted, list)
    assert isinstance(individual_converted, list)
    assert len(multi_converted) == len(levels)
    assert len(individual_converted) == len(levels)

    for from_multi, from_individual in zip(multi_converted, individual_converted):
        util_test.assert_lines(from_multi, line_type_to)
        util_test.assert_lines(from_individual, line_type_to)
        util_test.assert_equal_recursive(from_multi, from_individual)
