from contourpy import FillType, LineType
import numpy as np


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


def all_interps_str_value():
    return [
        ("Linear", 1),
        ("Log", 2),
    ]
