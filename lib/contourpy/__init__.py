from ._contourpy import (
    FillType, Interp, LineType, Mpl2014ContourGenerator,
    SerialContourGenerator)
from ._mpl2005 import Cntr as Mpl2005ContourGenerator
import numpy as np


def contour_generator(x, y, z, name=None, corner_mask=None, chunk_size=0,
                      fill_type=None, line_type=None, interp=Interp.Linear):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.ma.asarray(z, dtype=np.float64)  # Preserve mask if present.

    # Check arguments: z.
    if z.ndim != 2:
        raise TypeError(f'Input z must be 2D, not {z.ndim}D')
    if z.shape[0] < 2 or z.shape[1] < 2:
        raise TypeError('Input z must be at least a (2, 2) shaped array, '
                        f'but has shape {z.shape}')

    # Check arguments: x and y.
    if x.ndim != y.ndim:
        raise TypeError(f'Number of dimensions of x ({x.ndim}) and y '
                        f'({y.ndim}) do not match')
    if x.ndim == 0:
        x = np.arange(z.shape[1])
        y = np.arange(z.shape[0])
        x, y = np.meshgrid(x, y)
    elif x.ndim == 1:
        ny, nx = z.shape
        if len(x) != nx:
            raise TypeError(f'Length of x ({len(x)}) must match number of '
                            f'columns in z ({nx})')
        if len(y) != ny:
            raise TypeError(f'Length of y ({len(y)}) must match number of '
                            f'rows in z ({ny})')
        x, y = np.meshgrid(x, y)
    elif x.ndim == 2:
        if x.shape != z.shape:
            raise TypeError(
                f'Shapes of x {x.shape} and z {z.shape} do not match')
        if y.shape != z.shape:
            raise TypeError(
                f'Shapes of y {y.shape} and z {z.shape} do not match')
    else:
        raise TypeError(f'Inputs x and y must be None, 1D or 2D, not {x.ndim}D')

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
        if corner_mask is None:
            corner_mask = True

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
            x, y, z, mask, corner_mask, line_type, fill_type, interp,
            x_chunk_size=x_chunk_size, y_chunk_size=y_chunk_size)
    else:
        if chunk_size < 0:
            raise ValueError('chunk_size cannot be negative')

        if line_type not in (None, LineType.SeparateCodes):
            raise ValueError(f'{name} contour generator does not support line_type {line_type}')

        if fill_type not in (None, FillType.OuterCodes):
            raise ValueError(f'{name} contour generator does not support fill_type {fill_type}')

        if interp != Interp.Linear:
            raise ValueError(f'{name} contour generator does not support interp {interp}')

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
