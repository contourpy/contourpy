from contourpy import FillType, LineType


def all_names():
    return ['mpl2014', 'mpl2005', 'serial_corner']


def all_names_and_fill_types():
    return [
        ('mpl2005', FillType.OuterCodes),
        ('mpl2014', FillType.OuterCodes),
        ('serial_corner', FillType.OuterCodes),
        ('serial_corner', FillType.OuterOffsets),
        ('serial_corner', FillType.ChunkCombinedCodes),
        ('serial_corner', FillType.ChunkCombinedOffsets),
        ('serial_corner', FillType.ChunkCombinedCodesOffsets),
        ('serial_corner', FillType.ChunkCombinedOffsets2),
    ]


def all_names_and_line_types():
    return [
        ('mpl2005', LineType.SeparateCodes),
        ('mpl2014', LineType.SeparateCodes),
        ('serial_corner', LineType.Separate),
        ('serial_corner', LineType.SeparateCodes),
        ('serial_corner', LineType.ChunkCombinedCodes),
        ('serial_corner', LineType.ChunkCombinedOffsets),
    ]


def corner_mask_names():
    return ['mpl2014', 'serial_corner']


def all_fill_types_str_value():
    return [
        ('OuterCodes', 201),
        ('OuterOffsets', 202),
        ('ChunkCombinedCodes', 203),
        ('ChunkCombinedOffsets', 204),
        ('ChunkCombinedCodesOffsets', 205),
        ('ChunkCombinedOffsets2', 206),
    ]


def all_line_types_str_value():
    return [
        ('Separate', 101),
        ('SeparateCodes', 102),
        ('ChunkCombinedCodes', 103),
        ('ChunkCombinedOffsets', 104),
    ]


def all_interps_str_value():
    return [
        ('Linear', 1),
        ('Log', 2),
    ]
