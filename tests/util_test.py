from contourpy import FillType, LineType


def all_names():
    return ['mpl2014', 'mpl2005', 'serial']


def all_names_and_fill_types():
    return [
        ('mpl2005', FillType.OuterCodes),
        ('mpl2014', FillType.OuterCodes),
        ('serial', FillType.OuterCodes),
        ('serial', FillType.OuterOffsets),
        ('serial', FillType.ChunkCombinedCodes),
        ('serial', FillType.ChunkCombinedOffsets),
        ('serial', FillType.ChunkCombinedCodesOffsets),
        ('serial', FillType.ChunkCombinedOffsets2),
    ]


def all_names_and_line_types():
    return [
        ('mpl2005', LineType.Separate),
        ('mpl2014', LineType.Separate),
        ('serial', LineType.Separate),
        ('serial', LineType.SeparateCodes),
        ('serial', LineType.ChunkCombinedCodes),
        ('serial', LineType.ChunkCombinedOffsets),
    ]


def corner_mask_names():
    return ['mpl2014']


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
