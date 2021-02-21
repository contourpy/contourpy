import numpy as np


def random_uniform(shape, seed=2187, mask_fraction=0.0):
    ny, nx = shape
    x = np.linspace(0.0, 1.0, nx)
    y = np.linspace(0.0, 1.0, ny)
    x, y = np.meshgrid(x, y)

    np.random.seed(seed)
    z = np.random.uniform(size=shape)

    if mask_fraction > 0.0:
        mask_fraction = min(mask_fraction, 0.99)
        mask = np.random.uniform(size=shape) < mask_fraction
        z = np.ma.array(z, mask=mask)

    return x, y, z
