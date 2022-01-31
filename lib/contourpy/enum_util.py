from ._contourpy import FillType, LineType, ZInterp


def as_fill_type(fill_type):
    if isinstance(fill_type, str):
        fill_type = FillType.__members__[fill_type]
    return fill_type


def as_line_type(line_type):
    if isinstance(line_type, str):
        line_type = LineType.__members__[line_type]
    return line_type


def as_z_interp(z_interp):
    if isinstance(z_interp, str):
        z_interp = ZInterp.__members__[z_interp]
    return z_interp
