import numpy as np


def random_uniform(shape, seed=2187, mask_fraction=0.0):
    ny, nx = shape
    x = np.arange(nx, dtype=np.float64)
    y = np.arange(ny, dtype=np.float64)
    x, y = np.meshgrid(x, y)

    rng = np.random.default_rng(seed)
    z = rng.uniform(size=shape)

    if mask_fraction > 0.0:
        mask_fraction = min(mask_fraction, 0.99)
        mask = rng.uniform(size=shape) < mask_fraction
        z = np.ma.array(z, mask=mask)

    return x, y, z
