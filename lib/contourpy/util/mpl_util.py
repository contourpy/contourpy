import numpy as np


def mpl_codes_to_offsets(codes):
    offsets = np.nonzero(codes == 1)[0]
    offsets = np.append(offsets, len(codes))
    return offsets


def offsets_to_mpl_codes(offsets):
    codes = np.full(offsets[-1]-offsets[0], 2, dtype=np.uint8)  # LINETO = 2
    codes[offsets[:-1]] = 1  # MOVETO = 1
    codes[offsets[1:]-1] = 79  # CLOSEPOLY 79
    return codes
