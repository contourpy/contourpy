from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast, overload

import numpy as np

from contourpy import FillType, LineType, max_threads

if TYPE_CHECKING:
    import numpy.typing as npt

    import contourpy._contourpy as cpy


point_dtype = np.float64
code_dtype = np.uint8
offset_dtype = np.uint32


def all_class_names() -> list[str]:
    return [
        "Mpl2005ContourGenerator",
        "Mpl2014ContourGenerator",
        "SerialContourGenerator",
        "ThreadedContourGenerator",
    ]


def all_names(exclude: str | None = None) -> list[str]:
    all_ = ["mpl2005", "mpl2014", "serial", "threaded"]
    if exclude is not None:
        all_.remove(exclude)
    return all_


def all_names_and_fill_types() -> list[tuple[str, FillType]]:
    return [
        ("mpl2005", FillType.OuterCode),
        ("mpl2014", FillType.OuterCode),
        ("serial", FillType.OuterCode),
        ("serial", FillType.OuterOffset),
        ("serial", FillType.ChunkCombinedCode),
        ("serial", FillType.ChunkCombinedOffset),
        ("serial", FillType.ChunkCombinedCodeOffset),
        ("serial", FillType.ChunkCombinedOffsetOffset),
        ("threaded", FillType.OuterCode),
        ("threaded", FillType.OuterOffset),
        ("threaded", FillType.ChunkCombinedCode),
        ("threaded", FillType.ChunkCombinedOffset),
        ("threaded", FillType.ChunkCombinedCodeOffset),
        ("threaded", FillType.ChunkCombinedOffsetOffset),
    ]


def all_names_and_line_types() -> list[tuple[str, LineType]]:
    return [
        ("mpl2005", LineType.SeparateCode),
        ("mpl2014", LineType.SeparateCode),
        ("serial", LineType.Separate),
        ("serial", LineType.SeparateCode),
        ("serial", LineType.ChunkCombinedCode),
        ("serial", LineType.ChunkCombinedOffset),
        ("threaded", LineType.Separate),
        ("threaded", LineType.SeparateCode),
        ("threaded", LineType.ChunkCombinedCode),
        ("threaded", LineType.ChunkCombinedOffset),
    ]


def corner_mask_names() -> list[str]:
    return ["mpl2014", "serial", "threaded"]


def quad_as_tri_names() -> list[str]:
    return ["serial", "threaded"]


def all_fill_types_str_value() -> list[tuple[str, int]]:
    return [
        ("OuterCode", 201),
        ("OuterOffset", 202),
        ("ChunkCombinedCode", 203),
        ("ChunkCombinedOffset", 204),
        ("ChunkCombinedCodeOffset", 205),
        ("ChunkCombinedOffsetOffset", 206),
    ]


def all_line_types_str_value() -> list[tuple[str, int]]:
    return [
        ("Separate", 101),
        ("SeparateCode", 102),
        ("ChunkCombinedCode", 103),
        ("ChunkCombinedOffset", 104),
    ]


def all_z_interps_str_value() -> list[tuple[str, int]]:
    return [
        ("Linear", 1),
        ("Log", 2),
    ]


def thread_counts() -> list[int]:
    thread_counts = [2, 3]
    return list(filter(lambda n: n <= max(max_threads(), 1), thread_counts))


def assert_point_array(points: cpy.PointArray) -> int:
    assert isinstance(points, np.ndarray)
    assert points.dtype == point_dtype
    assert points.ndim == 2
    assert points.shape[1] == 2
    npoints = points.shape[0]
    assert npoints >= 1
    return npoints


def assert_code_array(codes: cpy.CodeArray, npoints: int) -> None:
    assert isinstance(codes, np.ndarray)
    assert codes.dtype == code_dtype
    assert codes.ndim == 1
    assert len(codes) == npoints
    assert codes[0] == 1


def assert_offset_array(offsets: cpy.OffsetArray, max_offset: int) -> int:
    assert isinstance(offsets, np.ndarray)
    assert offsets.dtype == offset_dtype
    assert offsets.ndim == 1
    assert len(offsets) > 1
    assert offsets[0] == 0
    assert offsets[-1] == max_offset
    assert np.all(np.diff(offsets) > 0)
    return len(offsets)


def assert_filled(filled: cpy.FillReturn, fill_type: FillType) -> None:
    if fill_type == FillType.OuterCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterCode, filled)
        assert isinstance(filled, tuple) and len(filled) == 2
        polygons, codes = filled
        assert isinstance(polygons, list)
        assert isinstance(codes, list)
        assert len(polygons) == len(codes)
        for polygon, code in zip(polygons, codes):
            npoints = assert_point_array(polygon)
            assert_code_array(code, npoints)
    elif fill_type == FillType.OuterOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterOffset, filled)
        assert isinstance(filled, tuple) and len(filled) == 2
        polygons, offsets = filled
        assert isinstance(polygons, list)
        assert isinstance(offsets, list)
        assert len(polygons) == len(offsets)
        for polygon, offset in zip(polygons, offsets):
            npoints = assert_point_array(polygon)
            assert_offset_array(offset, npoints)
    elif fill_type == FillType.ChunkCombinedCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCode, filled)
        assert isinstance(filled, tuple) and len(filled) == 2
        chunk_polygons, chunk_codes = filled
        assert isinstance(chunk_polygons, list)
        assert isinstance(chunk_codes, list)
        assert len(chunk_polygons) == len(chunk_codes)
        for polygons_or_none, codes_or_none in zip(chunk_polygons, chunk_codes):
            if polygons_or_none is None:
                assert codes_or_none is None
            else:
                if TYPE_CHECKING:
                    assert codes_or_none is not None
                npoints = assert_point_array(polygons_or_none)
                assert_code_array(codes_or_none, npoints)
    elif fill_type == FillType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffset, filled)
        assert isinstance(filled, tuple) and len(filled) == 2
        chunk_polygons, chunk_offsets = filled
        assert isinstance(chunk_polygons, list)
        assert isinstance(chunk_offsets, list)
        assert len(chunk_polygons) == len(chunk_offsets)
        for polygons_or_none, offsets_or_none in zip(chunk_polygons, chunk_offsets):
            if polygons_or_none is None:
                assert offsets_or_none is None
            else:
                if TYPE_CHECKING:
                    assert offsets_or_none is not None
                npoints = assert_point_array(polygons_or_none)
                assert_offset_array(offsets_or_none, npoints)
    elif fill_type == FillType.ChunkCombinedCodeOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCodeOffset, filled)
        assert isinstance(filled, tuple) and len(filled) == 3
        chunk_polygons, chunk_codes, chunk_outer_offsets = filled
        assert isinstance(chunk_polygons, list)
        assert isinstance(chunk_codes, list)
        assert isinstance(chunk_outer_offsets, list)
        assert len(chunk_polygons) == len(chunk_codes) == len(chunk_outer_offsets)
        for polygons_or_none, codes_or_none, outer_offsets_or_none in zip(
                chunk_polygons, chunk_codes, chunk_outer_offsets):
            if polygons_or_none is None:
                assert codes_or_none is None and outer_offsets_or_none is None
            else:
                if TYPE_CHECKING:
                    assert codes_or_none is not None and outer_offsets_or_none is not None
                npoints = assert_point_array(polygons_or_none)
                assert_code_array(codes_or_none, npoints)
                assert_offset_array(outer_offsets_or_none, npoints)
    elif fill_type == FillType.ChunkCombinedOffsetOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffsetOffset, filled)
        assert isinstance(filled, tuple) and len(filled) == 3
        chunk_polygons, chunk_offsets, chunk_outer_offsets = filled
        assert isinstance(chunk_polygons, list)
        assert isinstance(chunk_offsets, list)
        assert isinstance(chunk_outer_offsets, list)
        assert len(chunk_polygons) == len(chunk_offsets) == len(chunk_outer_offsets)
        for polygons_or_none, offsets_or_none, outer_offsets_or_none in zip(
                chunk_polygons, chunk_offsets, chunk_outer_offsets):
            if polygons_or_none is None:
                assert offsets_or_none is None and outer_offsets_or_none is None
            else:
                if TYPE_CHECKING:
                    assert offsets_or_none is not None and outer_offsets_or_none is not None
                npoints = assert_point_array(polygons_or_none)
                noffsets = assert_offset_array(offsets_or_none, npoints)
                assert_offset_array(outer_offsets_or_none, noffsets-1)
    else:
        raise RuntimeError(f"Unexpected fill_type {fill_type}")


def assert_lines(lines: cpy.LineReturn, line_type: LineType) -> None:
    if line_type == LineType.Separate:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_Separate, lines)
        assert isinstance(lines, list)
        for line in lines:
            assert_point_array(line)
    elif line_type == LineType.SeparateCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_SeparateCode, lines)
        assert isinstance(lines, tuple) and len(lines) == 2
        lines, codes = lines
        assert isinstance(lines, list)
        assert isinstance(codes, list)
        assert len(lines) == len(codes)
        for line, code in zip(lines, codes):
            npoints = assert_point_array(line)
            assert_code_array(code, npoints)
    elif line_type == LineType.ChunkCombinedCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedCode, lines)
        assert isinstance(lines, tuple) and len(lines) == 2
        chunk_lines, chunk_codes = lines
        assert isinstance(chunk_lines, list)
        assert isinstance(chunk_codes, list)
        assert len(chunk_lines) == len(chunk_codes)
        for lines_or_none, codes_or_none in zip(chunk_lines, chunk_codes):
            if lines_or_none is None:
                assert codes_or_none is None
            else:
                if TYPE_CHECKING:
                    assert codes_or_none is not None
                npoints = assert_point_array(lines_or_none)
                assert_code_array(codes_or_none, npoints)
    elif line_type == LineType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedOffset, lines)
        assert isinstance(lines, tuple) and len(lines) == 2
        chunk_lines, chunk_offsets = lines
        assert isinstance(chunk_lines, list)
        assert isinstance(chunk_offsets, list)
        assert len(chunk_lines) == len(chunk_offsets)
        for lines_or_none, offsets_or_none in zip(chunk_lines, chunk_offsets):
            if lines_or_none is None:
                assert offsets_or_none is None
            else:
                if TYPE_CHECKING:
                    assert offsets_or_none is not None
                npoints = assert_point_array(lines_or_none)
                assert_offset_array(offsets_or_none, npoints)
    else:
        raise RuntimeError(f"Unexpected line_type {line_type}")


@overload
def sort_by_first_xy(lines: list[cpy.PointArray]) -> list[cpy.PointArray]: ...


@overload
def sort_by_first_xy(
    lines: list[cpy.PointArray], others: list[npt.NDArray[Any]],
) -> tuple[list[cpy.PointArray], list[npt.NDArray[Any]]]: ...


def sort_by_first_xy(
    lines: list[cpy.PointArray], others: list[npt.NDArray[Any]] | None = None,
) -> list[cpy.PointArray] | tuple[list[cpy.PointArray], list[npt.NDArray[Any]]]:
    first_xy = np.array([line[0] for line in lines])
    order = np.lexsort((first_xy[:, 1], first_xy[:, 0]))
    lines = [lines[o] for o in order]
    if others is None:
        return lines
    else:
        others = [others[o] for o in order]
        return lines, others
