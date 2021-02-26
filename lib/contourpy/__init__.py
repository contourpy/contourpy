from ._contourpy import Mpl2014ContourGenerator
from ._mpl2005 import Cntr as Mpl2005ContourGenerator
import numpy as np


def contour_generator(x, y, z, corner_mask=True, chunk_size=0):
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

    if chunk_size < 0:
        raise ValueError('chunk_size cannot be negative')

    # Extract optional mask from z array.
    mask = None
    if np.ma.is_masked(z):
        mask = np.ma.getmask(z)

    # Check mask shape just in case.
    if mask is not None and mask.shape != z.shape:
        raise ValueError('If mask is set it must be a 2D array with the same shape as z')

#    cont_gen = Mpl2014ContourGenerator(x, y, z, mask, corner_mask=corner_mask,
#                                       chunk_size=chunk_size)

    # No corner mask here...
    #cont_gen = Mpl2005ContourGenerator(x, y, z, mask, chunk_size=chunk_size)
    cont_gen = Mpl2005ContourGenerator(x, y, z, mask)

    return cont_gen
