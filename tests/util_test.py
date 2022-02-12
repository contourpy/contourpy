import numpy as np

from contourpy import FillType, LineType


point_dtype = np.float64
code_dtype = np.uint8
offset_dtype = np.uint32


def all_class_names():
    return [
        "Mpl2005ContourGenerator",
        "Mpl2014ContourGenerator",
        "SerialContourGenerator",
        "ThreadedContourGenerator",
    ]


def all_names(exclude=None):
    all_ = ["mpl2005", "mpl2014", "serial", "threaded"]
    if exclude is not None:
        all_.remove(exclude)
    return all_


def all_names_and_fill_types():
    return [
        ("mpl2005", FillType.OuterCodes),
        ("mpl2014", FillType.OuterCodes),
        ("serial", FillType.OuterCodes),
        ("serial", FillType.OuterOffsets),
        ("serial", FillType.ChunkCombinedCodes),
        ("serial", FillType.ChunkCombinedOffsets),
        ("serial", FillType.ChunkCombinedCodesOffsets),
        ("serial", FillType.ChunkCombinedOffsets2),
        ("threaded", FillType.OuterCodes),
        ("threaded", FillType.OuterOffsets),
        ("threaded", FillType.ChunkCombinedCodes),
        ("threaded", FillType.ChunkCombinedOffsets),
        ("threaded", FillType.ChunkCombinedCodesOffsets),
        ("threaded", FillType.ChunkCombinedOffsets2),
    ]


def all_names_and_line_types():
    return [
        ("mpl2005", LineType.SeparateCodes),
        ("mpl2014", LineType.SeparateCodes),
        ("serial", LineType.Separate),
        ("serial", LineType.SeparateCodes),
        ("serial", LineType.ChunkCombinedCodes),
        ("serial", LineType.ChunkCombinedOffsets),
        ("threaded", LineType.Separate),
        ("threaded", LineType.SeparateCodes),
        ("threaded", LineType.ChunkCombinedCodes),
        ("threaded", LineType.ChunkCombinedOffsets),
    ]


def corner_mask_names():
    return ["mpl2014", "serial", "threaded"]


def quad_as_tri_names():
    return ["serial", "threaded"]


def all_fill_types_str_value():
    return [
        ("OuterCodes", 201),
        ("OuterOffsets", 202),
        ("ChunkCombinedCodes", 203),
        ("ChunkCombinedOffsets", 204),
        ("ChunkCombinedCodesOffsets", 205),
        ("ChunkCombinedOffsets2", 206),
    ]


def all_line_types_str_value():
    return [
        ("Separate", 101),
        ("SeparateCodes", 102),
        ("ChunkCombinedCodes", 103),
        ("ChunkCombinedOffsets", 104),
    ]


def all_z_interps_str_value():
    return [
        ("Linear", 1),
        ("Log", 2),
    ]


def assert_point_array(points):
    assert isinstance(points, np.ndarray)
    assert points.dtype == point_dtype
    assert points.ndim == 2
    assert points.shape[1] == 2
    npoints = points.shape[0]
    assert npoints >= 1
    return npoints


def assert_code_array(codes, npoints):
    assert isinstance(codes, np.ndarray)
    assert codes.dtype == code_dtype
    assert codes.ndim == 1
    assert len(codes) == npoints
    assert codes[0] == 1


def assert_offset_array(offsets, max_offset):
    assert isinstance(offsets, np.ndarray)
    assert offsets.dtype == offset_dtype
    assert offsets.ndim == 1
    assert len(offsets) > 1
    assert offsets[0] == 0
    assert offsets[-1] == max_offset
    assert np.all(np.diff(offsets) > 0)
    return len(offsets)


def assert_filled(filled, fill_type):
    if fill_type == FillType.OuterCodes:
        assert isinstance(filled, tuple) and len(filled) == 2
        polygons, codes = filled
        assert isinstance(polygons, list)
        assert isinstance(codes, list)
        assert len(polygons) == len(codes)
        for polygon, code in zip(polygons, codes):
            npoints = assert_point_array(polygon)
            assert_code_array(code, npoints)
    elif fill_type == FillType.OuterOffsets:
        assert isinstance(filled, tuple) and len(filled) == 2
        polygons, offsets = filled
        assert isinstance(polygons, list)
        assert isinstance(offsets, list)
        assert len(polygons) == len(offsets)
        for polygon, offset in zip(polygons, offsets):
            npoints = assert_point_array(polygon)
            assert_offset_array(offset, npoints)
    elif fill_type == FillType.ChunkCombinedCodes:
        assert isinstance(filled, tuple) and len(filled) == 2
        polygons, codes = filled
        assert isinstance(polygons, list)
        assert isinstance(codes, list)
        assert len(polygons) == len(codes)
        for polygon, code in zip(polygons, codes):
            if polygon is None:
                assert code is None
            else:
                npoints = assert_point_array(polygon)
                assert_code_array(code, npoints)
    elif fill_type == FillType.ChunkCombinedOffsets:
        assert isinstance(filled, tuple) and len(filled) == 2
        polygons, offsets = filled
        assert isinstance(polygons, list)
        assert isinstance(offsets, list)
        assert len(polygons) == len(offsets)
        for polygon, offset in zip(polygons, offsets):
            if polygon is None:
                assert offset is None
            else:
                npoints = assert_point_array(polygon)
                assert_offset_array(offset, npoints)
    elif fill_type == FillType.ChunkCombinedCodesOffsets:
        assert isinstance(filled, tuple) and len(filled) == 3
        polygons, codes, outer_offsets = filled
        assert isinstance(polygons, list)
        assert isinstance(codes, list)
        assert isinstance(outer_offsets, list)
        assert len(polygons) == len(codes) == len(outer_offsets)
        for polygon, code, outer_offset in zip(polygons, codes, outer_offsets):
            if polygon is None:
                assert code is None and outer_offset is None
            else:
                npoints = assert_point_array(polygon)
                assert_code_array(code, npoints)
                assert_offset_array(outer_offset, npoints)
    elif fill_type == FillType.ChunkCombinedOffsets2:
        assert isinstance(filled, tuple) and len(filled) == 3
        polygons, offsets, outer_offsets = filled
        assert isinstance(polygons, list)
        assert isinstance(offsets, list)
        assert isinstance(outer_offsets, list)
        assert len(polygons) == len(offsets) == len(outer_offsets)
        for polygon, offset, outer_offset in zip(polygons, offsets, outer_offsets):
            if polygon is None:
                assert offset is None and outer_offset is None
            else:
                npoints = assert_point_array(polygon)
                noffsets = assert_offset_array(offset, npoints)
                assert_offset_array(outer_offset, noffsets-1)
    else:
        raise RuntimeError(f"Unexpected fill_type {fill_type}")


def assert_lines(lines, line_type):
    if line_type == LineType.Separate:
        assert isinstance(lines, list)
        for line in lines:
            assert_point_array(line)
    elif line_type == LineType.SeparateCodes:
        assert isinstance(lines, tuple) and len(lines) == 2
        lines, codes = lines
        assert isinstance(lines, list)
        assert isinstance(codes, list)
        assert len(lines) == len(codes)
        for line, code in zip(lines, codes):
            npoints = assert_point_array(line)
            assert_code_array(code, npoints)
    elif line_type == LineType.ChunkCombinedCodes:
        assert isinstance(lines, tuple) and len(lines) == 2
        points, codes = lines
        assert isinstance(points, list)
        assert isinstance(codes, list)
        assert len(points) == len(codes)
        for line, code in zip(points, codes):
            if line is None:
                assert code is None
            else:
                npoints = assert_point_array(line)
                assert_code_array(code, npoints)
    elif line_type == LineType.ChunkCombinedOffsets:
        assert isinstance(lines, tuple) and len(lines) == 2
        points, offsets = lines
        assert isinstance(points, list)
        assert isinstance(offsets, list)
        assert len(points) == len(offsets)
        for line, offset in zip(points, offsets):
            if line is None:
                assert offset is None
            else:
                npoints = assert_point_array(line)
                assert_offset_array(offset, npoints)
    else:
        raise RuntimeError(f"Unexpected line_type {line_type}")
