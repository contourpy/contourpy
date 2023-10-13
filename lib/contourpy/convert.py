from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, cast

import numpy as np

from contourpy._contourpy import FillType, LineType
from contourpy.enum_util import as_fill_type, as_line_type
from contourpy.types import CLOSEPOLY, LINETO, MOVETO, code_dtype, offset_dtype

if TYPE_CHECKING:
    import numpy.typing as npt

    import contourpy._contourpy as cpy

    T = TypeVar("T", bound=np.generic)  # Type for generic np.ndarray


def _codes_from_offsets(offsets: cpy.OffsetArray) -> cpy.CodeArray:
    # All polygons are closed.
    n = offsets[-1]
    codes = np.full(n, LINETO, dtype=code_dtype)
    codes[offsets[:-1]] = MOVETO
    codes[offsets[1:] - 1] = CLOSEPOLY
    return codes


def _codes_from_offsets_and_points(
    offsets: cpy.OffsetArray,
    points: cpy.PointArray,
) -> cpy.CodeArray:
    # Use start and end points to determine if lines are closed or not.
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


def _concat_offsets(list_of_offsets: list[cpy.OffsetArray]) -> cpy.OffsetArray:
    n = len(list_of_offsets)
    cumulative_offsets = np.cumsum([offsets[-1] for offsets in list_of_offsets])
    ret: cpy.OffsetArray = np.concatenate(
        (list_of_offsets[0],
         *(list_of_offsets[i+1][1:] + cumulative_offsets[i] for i in range(n-1)))
    )
    return ret


def _offsets_from_codes(codes: cpy.CodeArray) -> cpy.OffsetArray:
    return np.append(np.nonzero(codes == MOVETO)[0], len(codes)).astype(offset_dtype)


def _offsets_from_lengths(seq: list[cpy.PointArray]) -> cpy.OffsetArray:
    return np.cumsum([0] + [len(line) for line in seq], dtype=offset_dtype)


def _outer_offsets_from_list_of_codes(seq: list[cpy.CodeArray]) -> cpy.OffsetArray:
    return np.cumsum([0] + [np.count_nonzero(codes == MOVETO) for codes in seq], dtype=offset_dtype)


def _outer_offsets_from_list_of_offsets(seq: list[cpy.OffsetArray]) -> cpy.OffsetArray:
    return np.cumsum([0] + [len(offsets)-1 for offsets in seq], dtype=offset_dtype)


def _split_by_offsets(array: npt.NDArray[T], offsets: cpy.OffsetArray) -> list[npt.NDArray[T]]:
    if len(offsets) > 2:
        return np.split(array, offsets[1:-1])
    else:
        return [array]


def _convert_filled_from_OuterCode(
    filled: cpy.FillReturn_OuterCode,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.OuterCode:
        return filled
    elif fill_type_to == FillType.OuterOffset:
        return (filled[0], [_offsets_from_codes(codes) for codes in filled[1]])

    if len(filled[0]) > 0:
        points = np.concatenate(filled[0])
        codes = np.concatenate(filled[1])
    else:
        points = None
        codes = None

    if fill_type_to == FillType.ChunkCombinedCode:
        return ([points], [codes])
    elif fill_type_to == FillType.ChunkCombinedOffset:
        return ([points], [None if codes is None else _offsets_from_codes(codes)])
    elif fill_type_to == FillType.ChunkCombinedCodeOffset:
        outer_offsets = None if points is None else _offsets_from_lengths(filled[0])
        ret1: cpy.FillReturn_ChunkCombinedCodeOffset = ([points], [codes], [outer_offsets])
        return ret1
    elif fill_type_to == FillType.ChunkCombinedOffsetOffset:
        if codes is None:
            ret2: cpy.FillReturn_ChunkCombinedOffsetOffset = ([None], [None], [None])
        else:
            offsets = _offsets_from_codes(codes)
            outer_offsets = _outer_offsets_from_list_of_codes(filled[1])
            ret2 = ([points], [offsets], [outer_offsets])
        return ret2
    else:
        raise ValueError(f"Invalid FillType {fill_type_to}")


def _convert_filled_from_OuterOffset(
    filled: cpy.FillReturn_OuterOffset,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.OuterCode:
        separate_codes = [_codes_from_offsets(offsets) for offsets in filled[1]]
        return (filled[0], separate_codes)
    elif fill_type_to == FillType.OuterOffset:
        return filled

    if len(filled[0]) > 0:
        points = np.concatenate(filled[0])
        offsets = _concat_offsets(filled[1])
    else:
        points = None
        offsets = None

    if fill_type_to == FillType.ChunkCombinedCode:
        return ([points], [None if offsets is None else _codes_from_offsets(offsets)])
    elif fill_type_to == FillType.ChunkCombinedOffset:
        return ([points], [offsets])
    elif fill_type_to == FillType.ChunkCombinedCodeOffset:
        if offsets is None:
            ret1: cpy.FillReturn_ChunkCombinedCodeOffset = ([None], [None], [None])
        else:
            ret1 = ([points], [_codes_from_offsets(offsets)], [_offsets_from_lengths(filled[0])])
        return ret1
    elif fill_type_to == FillType.ChunkCombinedOffsetOffset:
        if points is None:
            ret2: cpy.FillReturn_ChunkCombinedOffsetOffset = ([None], [None], [None])
        else:
            ret2 = ([points], [offsets], [_outer_offsets_from_list_of_offsets(filled[1])])
        return ret2
    else:
        raise ValueError(f"Invalid FillType {fill_type_to}")


def _convert_filled_from_ChunkCombinedCode(
    filled: cpy.FillReturn_ChunkCombinedCode,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.ChunkCombinedCode:
        return filled
    elif fill_type_to == FillType.ChunkCombinedOffset:
        codes = [None if codes is None else _offsets_from_codes(codes) for codes in filled[1]]
        return (filled[0], codes)
    else:
        raise ValueError(
            f"Conversion from {FillType.ChunkCombinedCode} to {fill_type_to} not supported")


def _convert_filled_from_ChunkCombinedOffset(
    filled: cpy.FillReturn_ChunkCombinedOffset,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.ChunkCombinedCode:
        chunk_codes: list[cpy.CodeArray | None] = []
        for points, offsets in zip(*filled):
            if points is None:
                chunk_codes.append(None)
            else:
                if TYPE_CHECKING:
                    assert offsets is not None
                chunk_codes.append(_codes_from_offsets_and_points(offsets, points))
        return (filled[0], chunk_codes)
    elif fill_type_to == FillType.ChunkCombinedOffset:
        return filled
    else:
        raise ValueError(
            f"Conversion from {FillType.ChunkCombinedOffset} to {fill_type_to} not supported")


def _convert_filled_from_ChunkCombinedCodeOffset(
    filled: cpy.FillReturn_ChunkCombinedCodeOffset,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.OuterCode:
        separate_points = []
        separate_codes = []
        for points, codes, outer_offsets in zip(*filled):
            if points is not None:
                if TYPE_CHECKING:
                    assert codes is not None
                    assert outer_offsets is not None
                separate_points += _split_by_offsets(points, outer_offsets)
                separate_codes += _split_by_offsets(codes, outer_offsets)
        return (separate_points, separate_codes)
    elif fill_type_to == FillType.OuterOffset:
        separate_points = []
        separate_offsets = []
        for points, codes, outer_offsets in zip(*filled):
            if points is not None:
                if TYPE_CHECKING:
                    assert codes is not None
                    assert outer_offsets is not None
                separate_points += _split_by_offsets(points, outer_offsets)
                separate_codes = _split_by_offsets(codes, outer_offsets)
                separate_offsets += [_offsets_from_codes(c) for c in separate_codes]
        return (separate_points, separate_offsets)
    elif fill_type_to == FillType.ChunkCombinedCode:
        ret1: cpy.FillReturn_ChunkCombinedCode = (filled[0], filled[1])
        return ret1
    elif fill_type_to == FillType.ChunkCombinedOffset:
        all_offsets = [None if codes is None else _offsets_from_codes(codes) for codes in filled[1]]
        ret2: cpy.FillReturn_ChunkCombinedOffset = (filled[0], all_offsets)
        return ret2
    elif fill_type_to == FillType.ChunkCombinedCodeOffset:
        return filled
    elif fill_type_to == FillType.ChunkCombinedOffsetOffset:
        chunk_offsets: list[cpy.OffsetArray | None] = []
        chunk_outer_offsets: list[cpy.OffsetArray | None] = []
        for codes, outer_offsets in zip(*filled[1:]):
            if codes is None:  # Empty chunk.
                chunk_offsets.append(None)
                chunk_outer_offsets.append(None)
            else:
                if TYPE_CHECKING:
                    assert outer_offsets is not None
                offsets = _offsets_from_codes(codes)
                outer_offsets = np.array([np.nonzero(offsets == oo)[0][0] for oo in outer_offsets],
                                         dtype=offset_dtype)
                chunk_offsets.append(offsets)
                chunk_outer_offsets.append(outer_offsets)
        ret3: cpy.FillReturn_ChunkCombinedOffsetOffset = (
            filled[0], chunk_offsets, chunk_outer_offsets,
        )
        return ret3
    else:
        raise ValueError(f"Invalid FillType {fill_type_to}")


def _convert_filled_from_ChunkCombinedOffsetOffset(
    filled: cpy.FillReturn_ChunkCombinedOffsetOffset,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.OuterCode:
        separate_points = []
        separate_codes = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is not None:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                codes = _codes_from_offsets_and_points(offsets, points)
                outer_offsets = offsets[outer_offsets]
                separate_points += _split_by_offsets(points, outer_offsets)
                separate_codes += _split_by_offsets(codes, outer_offsets)
        return (separate_points, separate_codes)
    elif fill_type_to == FillType.OuterOffset:
        separate_points = []
        separate_offsets = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is not None:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                if len(outer_offsets) > 2:
                    separate_offsets += [offsets[s:e+1] - offsets[s] for s, e in
                                         zip(outer_offsets[:-1], outer_offsets[1:])]
                else:
                    separate_offsets.append(offsets)
                separate_points += _split_by_offsets(points, offsets[outer_offsets])
        return (separate_points, separate_offsets)
    elif fill_type_to == FillType.ChunkCombinedCode:
        chunk_codes: list[cpy.CodeArray | None] = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is None:
                chunk_codes.append(None)
            else:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                chunk_codes.append(_codes_from_offsets_and_points(offsets, points))
        ret1: cpy.FillReturn_ChunkCombinedCode = (filled[0], chunk_codes)
        return ret1
    elif fill_type_to == FillType.ChunkCombinedOffset:
        return (filled[0], filled[1])
    elif fill_type_to == FillType.ChunkCombinedCodeOffset:
        chunk_codes = []
        chunk_outer_offsets: list[cpy.OffsetArray | None] = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is None:
                chunk_codes.append(None)
                chunk_outer_offsets.append(None)
            else:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                chunk_codes.append(_codes_from_offsets_and_points(offsets, points))
                chunk_outer_offsets.append(offsets[outer_offsets])
        ret2: cpy.FillReturn_ChunkCombinedCodeOffset = (filled[0], chunk_codes, chunk_outer_offsets)
        return ret2
    elif fill_type_to == FillType.ChunkCombinedOffsetOffset:
        return filled
    else:
        raise ValueError(f"Invalid FillType {fill_type_to}")


def convert_fill_type(
    filled: cpy.FillReturn,
    fill_type_from: FillType | str,
    fill_type_to:  FillType | str,
) -> cpy.FillReturn:
    """Return the specified filled contours converted to a different ``FillType``.

    Args:
        filled (sequence of arrays): Filled contour polygons to convert.
        fill_type_from (FillType or str): ``FillType`` to convert from.
        fill_type_to (FillType or str): ``FillType`` to convert to.

    Return:
        Converted filled contour polygons.

    When converting non-chunked fill types (``FillType.OuterCode`` or ``FillType.OuterOffset``) to
    chunked ones, all polygons are placed in the first chunk. When converting in the other
    direction, all chunk information is discarded. Converting a fill type that is not aware of the
    relationship between outer boundaries and contained holes (``FillType.ChunkCombinedCode`` or)
    ``FillType.ChunkCombinedOffset``) to one that is will raise a ``ValueError``.

    .. versionadded:: 1.1.2
    """
    fill_type_from = as_fill_type(fill_type_from)
    fill_type_to = as_fill_type(fill_type_to)

    if fill_type_from == FillType.OuterCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterCode, filled)
        return _convert_filled_from_OuterCode(filled, fill_type_to)
    elif fill_type_from == FillType.OuterOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterOffset, filled)
        return _convert_filled_from_OuterOffset(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCode, filled)
        return _convert_filled_from_ChunkCombinedCode(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffset, filled)
        return _convert_filled_from_ChunkCombinedOffset(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedCodeOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCodeOffset, filled)
        return _convert_filled_from_ChunkCombinedCodeOffset(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedOffsetOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffsetOffset, filled)
        return _convert_filled_from_ChunkCombinedOffsetOffset(filled, fill_type_to)
    else:
        raise ValueError(f"Invalid FillType {fill_type_from}")


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
            if points is not None:
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
            if points is not None:
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
        chunk_offsets = [None if codes is None else _offsets_from_codes(codes)
                         for codes in lines[1]]
        return (lines[0], chunk_offsets)
    else:
        raise ValueError(f"Invalid LineType {line_type_to}")


def _convert_lines_from_ChunkCombinedOffset(
        lines: cpy.LineReturn_ChunkCombinedOffset,
        line_type_to: LineType,
) -> cpy.LineReturn:
    if line_type_to in (LineType.Separate, LineType.SeparateCode):
        separate_lines = []
        for points, offsets in zip(*lines):
            if points is not None:
                if TYPE_CHECKING:
                    assert offsets is not None
                separate_lines += _split_by_offsets(points, offsets)
        if line_type_to == LineType.Separate:
            return separate_lines
        else:
            separate_codes = [_codes_from_points(line) for line in separate_lines]
            return (separate_lines, separate_codes)
    elif line_type_to == LineType.ChunkCombinedCode:
        chunk_codes: list[cpy.CodeArray | None] = []
        for points, offsets in zip(*lines):
            if points is None:  # Empty chunk.
                chunk_codes.append(None)
            else:
                if TYPE_CHECKING:
                    assert offsets is not None
                chunk_codes.append(_codes_from_offsets_and_points(offsets, points))
        return (lines[0], chunk_codes)
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
