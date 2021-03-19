from contourpy import FillType


def all_names():
    return ['mpl2014', 'mpl2005', 'serial']


def all_names_and_fill_types():
    return [
        ('mpl2014', FillType.OuterCodes),
        ('mpl2005', FillType.OuterCodes),
        ('serial', FillType.OuterCodes),
        ('serial', FillType.OuterOffsets),
        ('serial', FillType.CombinedCodes),
        ('serial', FillType.CombinedOffsets),
        ('serial', FillType.CombinedCodesOffsets),
        ('serial', FillType.CombinedOffsets2),
    ]


def corner_mask_names():
    return ['mpl2014']


def all_fill_types_str_value():
    return [
        ('OuterCodes', 1),
        ('OuterOffsets', 2),
        ('CombinedCodes', 3),
        ('CombinedOffsets', 4),
        ('CombinedCodesOffsets', 5),
        ('CombinedOffsets2', 6),
    ]


def all_line_types_str_value():
    return [
        ('Separate', 0),
    ]
