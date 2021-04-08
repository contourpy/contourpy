from ._contourpy import (
    FillType, LineType, Mpl2014ContourGenerator, SerialContourGenerator,
    SerialCornerContourGenerator)
from ._mpl2005 import Cntr as Mpl2005ContourGenerator
import numpy as np


def contour_generator(x, y, z, name=None, corner_mask=None, chunk_size=0,
                      fill_type=None, line_type=None):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.ma.asarray(z, dtype=np.float64)  # Preserve mask if present.

    # Check arguments.
    if x.ndim != 2 or y.ndim != 2 or z.ndim != 2:
        raise ValueError('x, y and z must all be 2D arrays')

    if x.shape != z.shape or y.shape != z.shape:
        raise ValueError('x, y and z arrays must have the same shape')

    if z.shape[0] < 2 or z.shape[1] < 2:
        raise ValueError('x, y and z must all be at least 2x2 arrays')

    # Extract optional mask from z array.
    mask = None
    if np.ma.is_masked(z):
        mask = np.ma.getmask(z)

    # Check mask shape just in case.
    if mask is not None and mask.shape != z.shape:
        raise ValueError('If mask is set it must be a 2D array with the same shape as z')

    # Default name.
    if name is None:
        name = 'mpl2014'

    if name == 'serial':
        if corner_mask:
            raise ValueError('serial contour generator does not support corner_mask=True')

        if line_type is None:
            line_type = SerialContourGenerator.default_line_type
        if not SerialContourGenerator.supports_line_type(line_type):
            raise ValueError(f'serial contour generator does not support line_type {line_type}')

        if fill_type is None:
            fill_type = SerialContourGenerator.default_fill_type
        if not SerialContourGenerator.supports_fill_type(fill_type):
            raise ValueError(f'serial contour generator does not support fill_type {fill_type}')

        if isinstance(chunk_size, tuple) and len(chunk_size) == 2:
            y_chunk_size, x_chunk_size = chunk_size
        else:
            y_chunk_size = x_chunk_size = chunk_size

        if x_chunk_size < 0 or y_chunk_size < 0:
            raise ValueError('chunk_size cannot be negative')

        cont_gen = SerialContourGenerator(
            x, y, z, mask, line_type, fill_type, x_chunk_size=x_chunk_size,
            y_chunk_size=y_chunk_size)
    elif name == 'serial_corner':
        if corner_mask is None:
            corner_mask = True

        if line_type is None:
            line_type = SerialCornerContourGenerator.default_line_type
        if not SerialCornerContourGenerator.supports_line_type(line_type):
            raise ValueError(f'serial_corner contour generator does not support line_type {line_type}')

        if fill_type is None:
            fill_type = SerialCornerContourGenerator.default_fill_type
        if not SerialCornerContourGenerator.supports_fill_type(fill_type):
            raise ValueError(f'serial_corner contour generator does not support fill_type {fill_type}')

        if isinstance(chunk_size, tuple) and len(chunk_size) == 2:
            y_chunk_size, x_chunk_size = chunk_size
        else:
            y_chunk_size = x_chunk_size = chunk_size

        if x_chunk_size < 0 or y_chunk_size < 0:
            raise ValueError('chunk_size cannot be negative')

        cont_gen = SerialCornerContourGenerator(
            x, y, z, mask, corner_mask, line_type, fill_type,
            x_chunk_size=x_chunk_size, y_chunk_size=y_chunk_size)
    else:
        if chunk_size < 0:
            raise ValueError('chunk_size cannot be negative')

        if line_type not in (None, LineType.SeparateCodes):
            raise ValueError(f'{name} contour generator does not support line_type {line_type}')

        if fill_type not in (None, FillType.OuterCodes):
            raise ValueError(f'{name} contour generator does not support fill_type {fill_type}')

        if name == 'mpl2014':
            if corner_mask is None:
                corner_mask = True
            cont_gen = Mpl2014ContourGenerator(
                x, y, z, mask, corner_mask=corner_mask, chunk_size=chunk_size)
        elif name == 'mpl2005':
            if corner_mask:
                raise ValueError('mpl2005 contour generator does not support corner_mask=True')
            cont_gen = Mpl2005ContourGenerator(
                x, y, z, mask, chunk_size=chunk_size)
        else:
            raise ValueError(f'Unrecognised contour generator name: {name}')

    return cont_gen
