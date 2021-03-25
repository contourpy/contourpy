from contourpy import FillType, LineType


def all_names():
    return ['mpl2014', 'mpl2005', 'serial']


def all_names_and_fill_types():
    return [
        ('mpl2005', FillType.OuterCodes),
        ('mpl2014', FillType.OuterCodes),
        ('serial', FillType.OuterCodes),
        ('serial', FillType.OuterOffsets),
        ('serial', FillType.CombinedCodes),
        ('serial', FillType.CombinedOffsets),
        ('serial', FillType.CombinedCodesOffsets),
        ('serial', FillType.CombinedOffsets2),
    ]


def all_names_and_line_types():
    return [
        ('mpl2005', LineType.Separate),
        ('mpl2014', LineType.Separate),
        ('serial', LineType.Separate),
        ('serial', LineType.SeparateCodes),
        ('serial', LineType.CombinedCodes),
        ('serial', LineType.CombinedOffsets),
    ]


def corner_mask_names():
    return ['mpl2014']


def all_fill_types_str_value():
    return [
        ('OuterCodes', 201),
        ('OuterOffsets', 202),
        ('CombinedCodes', 203),
        ('CombinedOffsets', 204),
        ('CombinedCodesOffsets', 205),
        ('CombinedOffsets2', 206),
    ]


def all_line_types_str_value():
    return [
        ('Separate', 101),
        ('SeparateCodes', 102),
        ('CombinedCodes', 103),
        ('CombinedOffsets', 104),
    ]
