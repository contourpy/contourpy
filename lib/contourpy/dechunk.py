from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np

from contourpy import FillType, LineType
from contourpy.enum_util import as_fill_type, as_line_type

if TYPE_CHECKING:
    import contourpy._contourpy as cpy


def _concat_codes(chunk_codes_or_none: list[cpy.CodeArray | None]) -> cpy.CodeArray | None:
    chunk_codes = [chunk for chunk in chunk_codes_or_none if chunk is not None]
    if not chunk_codes:
        return None
    return np.concatenate(chunk_codes)


def _concat_offsets(chunk_offsets_or_none: list[cpy.OffsetArray | None]) -> cpy.OffsetArray | None:
    chunk_offsets = [chunk for chunk in chunk_offsets_or_none if chunk is not None]
    if not chunk_offsets:
        return None
    nchunks = len(chunk_offsets)
    cumulative_offsets = np.cumsum([offsets[-1] for offsets in chunk_offsets])
    ret: cpy.OffsetArray = np.concatenate(
        (chunk_offsets[0],
         *(chunk_offsets[i+1][1:] + cumulative_offsets[i] for i in range(nchunks-1)))
    )
    return ret


def _concat_points(chunk_points_or_none: list[cpy.PointArray | None]) -> cpy.PointArray | None:
    chunk_points = [chunk for chunk in chunk_points_or_none if chunk is not None]
    if not chunk_points:
        return None
    return np.concatenate(chunk_points)


def dechunk_filled(filled: cpy.FillReturn, fill_type: FillType | str) -> cpy.FillReturn:
    """Return the specified filled contours with all chunked data moved into the first chunk.

    Filled contours that are not chunked (``FillType.OuterCode`` and ``FillType.OuterOffset``) and
    those that are but only contain a single chunk are returned unmodified. Individual polygons are
    unchanged, they are not geometrically combined.

    Args:
        filled (sequence of arrays): Filled contour data as returned by
            :func:`~contourpy.ContourGenerator.filled`.
        fill_type (FillType or str): Type of ``filled`` as enum or string equivalent.

    Return:
        Filled contours in a single chunk.

    .. versionadded:: 1.1.2
    """
    fill_type = as_fill_type(fill_type)

    if fill_type in (FillType.OuterCode, FillType.OuterOffset) or len(filled[0]) < 2:
        # No-op if fill_type is not chunked or there is just one chunk.
        return filled

    if TYPE_CHECKING:
        filled = cast(cpy.FillReturn_Chunk, filled)
    points = _concat_points(filled[0])

    if fill_type == FillType.ChunkCombinedCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCode, filled)
        if points is None:
            ret1: cpy.FillReturn_ChunkCombinedCode = ([None], [None])
        else:
            ret1 = ([points], [_concat_codes(filled[1])])
        return ret1
    elif fill_type == FillType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffset, filled)
        if points is None:
            ret2: cpy.FillReturn_ChunkCombinedOffset = ([None], [None])
        else:
            ret2 = ([points], [_concat_offsets(filled[1])])
        return ret2
    elif fill_type == FillType.ChunkCombinedCodeOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCodeOffset, filled)
        if points is None:
            ret3: cpy.FillReturn_ChunkCombinedCodeOffset = ([None], [None], [None])
        else:
            ret3 = ([points], [_concat_codes(filled[1])], [_concat_offsets(filled[2])])
        return ret3
    elif fill_type == FillType.ChunkCombinedOffsetOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffsetOffset, filled)
        if points is None:
            ret4: cpy.FillReturn_ChunkCombinedOffsetOffset = ([None], [None], [None])
        else:
            ret4 = ([points], [_concat_offsets(filled[1])], [_concat_offsets(filled[2])])
        return ret4
    else:
        raise ValueError(f"Invalid FillType {fill_type}")


def dechunk_lines(lines: cpy.LineReturn, line_type: LineType | str) -> cpy.LineReturn:
    """Return the specified contour lines with all chunked data moved into the first chunk.

    Contour lines that are not chunked (``LineType.Separate`` and ``LineType.SeparateCode``) and
    those that are but only contain a single chunk are returned unmodified. Individual lines are
    unchanged, they are not geometrically combined.

    Args:
        lines (sequence of arrays): Contour line data as returned by
            :func:`~contourpy.ContourGenerator.lines`.
        line_type (LineType or str): Type of ``lines`` as enum or string equivalent.

    Return:
        Contour lines in a single chunk.

    .. versionadded:: 1.1.2
    """
    line_type = as_line_type(line_type)

    if line_type in (LineType.Separate, LineType.SeparateCode) or len(lines[0]) < 2:
        # No-op if line_type is not chunked or there is just one chunk.
        return lines

    if TYPE_CHECKING:
        lines = cast(cpy.LineReturn_Chunk, lines)
    points = _concat_points(lines[0])

    if line_type == LineType.ChunkCombinedCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedCode, lines)
        if points is None:
            ret1: cpy.LineReturn_ChunkCombinedCode = ([None], [None])
        else:
            ret1 = ([points], [_concat_codes(lines[1])])
        return ret1
    elif line_type == LineType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedOffset, lines)
        if points is None:
            ret2: cpy.LineReturn_ChunkCombinedOffset = ([None], [None])
        else:
            ret2 = ([points], [_concat_offsets(lines[1])])
        return ret2
    else:
        raise ValueError(f"Invalid LineType {line_type}")
