from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np

from contourpy._contourpy import LineType
from contourpy.enum_util import as_line_type
from contourpy.types import CLOSEPOLY, LINETO, MOVETO, code_dtype, offset_dtype

if TYPE_CHECKING:
    import contourpy._contourpy as cpy


def _codes_from_offsets_and_points(
    offsets: cpy.OffsetArray,
    points: cpy.PointArray,
) -> cpy.CodeArray:
    codes = np.full(len(points), LINETO, dtype=code_dtype)
    codes[offsets[:-1]] = MOVETO

    end_offsets = offsets[1:] - 1
    closed = np.all(points[offsets[:-1]] == points[end_offsets], axis=1)
    codes[end_offsets[closed]] = CLOSEPOLY

    return codes


def _codes_from_points(points: cpy.PointArray) -> cpy.CodeArray:
    # points are for a single line, closed or open.
    n = len(points)
    codes = np.full(n, LINETO, dtype=code_dtype)
    codes[0] = MOVETO
    if np.all(points[0] == points[-1]):
        codes[-1] = CLOSEPOLY
    return codes


def _offsets_from_codes(codes: cpy.CodeArray) -> cpy.OffsetArray:
    return np.append(np.nonzero(codes == MOVETO)[0], len(codes)).astype(offset_dtype)


def _offsets_from_lengths(seq: list[cpy.PointArray]) -> cpy.OffsetArray:
    offsets = np.cumsum([len(line) for line in seq], dtype=offset_dtype)
    return np.insert(offsets, 0, 0)


def _convert_lines_from_Separate(
    lines: cpy.LineReturn_Separate,
    line_type_to: LineType,
) -> cpy.LineReturn:
    if line_type_to == LineType.Separate:
        return lines
    elif line_type_to == LineType.SeparateCode:
        separate_codes = [_codes_from_points(line) for line in lines]
        return (lines, separate_codes)
    elif line_type_to == LineType.ChunkCombinedCode:
        if not lines:
            ret1: cpy.LineReturn_ChunkCombinedCode = ([None], [None])
        else:
            points = np.concatenate(lines)
            offsets = _offsets_from_lengths(lines)
            codes = _codes_from_offsets_and_points(offsets, points)
            ret1 = ([points], [codes])
        return ret1
    elif line_type_to == LineType.ChunkCombinedOffset:
        if not lines:
            ret2: cpy.LineReturn_ChunkCombinedOffset = ([None], [None])
        else:
            offsets = _offsets_from_lengths(lines)
            ret2 = ([np.concatenate(lines)], [offsets])
        return ret2
    else:
        raise ValueError(f"Invalid LineType {line_type_to}")


def _convert_lines_from_SeparateCode(
    lines: cpy.LineReturn_SeparateCode,
    line_type_to: LineType,
) -> cpy.LineReturn:
    if line_type_to == LineType.Separate:
        # Drop codes.
        return lines[0]
    elif line_type_to == LineType.SeparateCode:
        return lines
    elif line_type_to == LineType.ChunkCombinedCode:
        if not lines[0]:
            ret1: cpy.LineReturn_ChunkCombinedCode = ([None], [None])
        else:
            ret1 = ([np.concatenate(lines[0])], [np.concatenate(lines[1])])
        return ret1
    elif line_type_to == LineType.ChunkCombinedOffset:
        if not lines[0]:
            ret2: cpy.LineReturn_ChunkCombinedOffset = ([None], [None])
        else:
            offsets = _offsets_from_lengths(lines[0])
            ret2 = ([np.concatenate(lines[0])], [offsets])
        return ret2
    else:
        raise ValueError(f"Invalid LineType {line_type_to}")


def _convert_lines_from_ChunkCombinedCode(
        lines: cpy.LineReturn_ChunkCombinedCode,
        line_type_to: LineType,
) -> cpy.LineReturn:
    if line_type_to == LineType.Separate:
        separate_lines = []
        for points, codes in zip(*lines):
            if points is None:  # Empty chunk.
                continue
            if TYPE_CHECKING:
                assert codes is not None
            split_at = np.nonzero(codes == MOVETO)[0]
            if len(split_at) > 1:
                separate_lines += np.split(points, split_at[1:])
            else:
                separate_lines.append(points)
        return separate_lines
    elif line_type_to == LineType.SeparateCode:
        separate_lines = []
        separate_codes = []
        for points, codes in zip(*lines):
            if points is None:  # Empty chunk.
                continue
            if TYPE_CHECKING:
                assert codes is not None
            split_at = np.nonzero(codes == MOVETO)[0]
            if len(split_at) > 1:
                separate_lines += np.split(points, split_at[1:])
                separate_codes += np.split(codes, split_at[1:])
            else:
                separate_lines.append(points)
                separate_codes.append(codes)
        return (separate_lines, separate_codes)
    elif line_type_to == LineType.ChunkCombinedCode:
        return lines
    elif line_type_to == LineType.ChunkCombinedOffset:
        all_points = lines[0]
        all_offsets: list[cpy.OffsetArray | None] = []
        for points, codes in zip(*lines):
            if points is None:  # Empty chunk.
                all_offsets.append(None)
                continue
            if TYPE_CHECKING:
                assert codes is not None
            all_offsets.append(_offsets_from_codes(codes))
        return (all_points, all_offsets)
    else:
        raise ValueError(f"Invalid LineType {line_type_to}")


def _convert_lines_from_ChunkCombinedOffset(
        lines: cpy.LineReturn_ChunkCombinedOffset,
        line_type_to: LineType,
) -> cpy.LineReturn:
    if line_type_to in (LineType.Separate, LineType.SeparateCode):
        separate_lines = []
        for points, offsets in zip(*lines):
            if points is None:  # Empty chunk.
                continue
            if TYPE_CHECKING:
                assert offsets is not None
            if len(offsets) > 2:
                separate_lines += np.split(points, offsets[1:-1])
            else:
                separate_lines.append(points)
        if line_type_to == LineType.Separate:
            return separate_lines
        else:
            separate_codes = [_codes_from_points(line) for line in separate_lines]
            return (separate_lines, separate_codes)
    elif line_type_to == LineType.ChunkCombinedCode:
        all_points = lines[0]
        all_codes: list[cpy.CodeArray | None] = []
        for points, offsets in zip(*lines):
            if points is None:  # Empty chunk.
                all_codes.append(None)
                continue
            if TYPE_CHECKING:
                assert offsets is not None
            all_codes.append(_codes_from_offsets_and_points(offsets, points))
        return (all_points, all_codes)
    elif line_type_to == LineType.ChunkCombinedOffset:
        return lines
    else:
        raise ValueError(f"Invalid LineType {line_type_to}")


def convert_line_type(
    lines: cpy.LineReturn,
    line_type_from: LineType | str,
    line_type_to:  LineType | str,
) -> cpy.LineReturn:
    """Return the specified contour lines converted to a different ``LineType``.

    Args:
        lines (sequence of arrays): Contour lines to convert.
        line_type_from (LineType or str): ``LineType`` to convert from.
        line_type_to (LineType or str): ``LineType`` to convert to.

    Return:
        Converted contour lines.

    When converting non-chunked line types (``LineType.Separate`` or ``LineType.SeparateCode``) to
    chunked ones (``LineType.ChunkCombinedCode`` or ``LineType.ChunkCombinedOffset``), all lines are
    placed in the first chunk. When converting in the other direction, all chunk information is
    discarded.

    .. versionadded:: 1.1.2
    """
    line_type_from = as_line_type(line_type_from)
    line_type_to = as_line_type(line_type_to)

    if line_type_from == LineType.Separate:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_Separate, lines)
        return _convert_lines_from_Separate(lines, line_type_to)
    elif line_type_from == LineType.SeparateCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_SeparateCode, lines)
        return _convert_lines_from_SeparateCode(lines, line_type_to)
    elif line_type_from == LineType.ChunkCombinedCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedCode, lines)
        return _convert_lines_from_ChunkCombinedCode(lines, line_type_to)
    elif line_type_from == LineType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedOffset, lines)
        return _convert_lines_from_ChunkCombinedOffset(lines, line_type_to)
    else:
        raise ValueError(f"Invalid LineType {line_type_from}")
