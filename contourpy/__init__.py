from _contourpy import Mpl2014ContourGenerator
import numpy as np


def get_contour_generator(x, y, z, corner_mask=True, chunk_size=0):
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

    cg = Mpl2014ContourGenerator(x, y, z, mask, corner_mask, chunk_size)

    return cg
