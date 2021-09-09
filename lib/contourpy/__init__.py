from .chunk import calc_chunk_sizes
from ._contourpy import (
    max_threads, FillType, LineType, Mpl2005ContourGenerator, Mpl2014ContourGenerator,
    SerialContourGenerator, ThreadedContourGenerator, ZInterp
)
from ._version import __version__
import numpy as np


__all__ = [
    "__version__",
    "contour_generator",
    "max_threads",
    "FillType",
    "LineType",
    "Mpl2005ContourGenerator",
    "Mpl2014ContourGenerator",
    "SerialContourGenerator",
    "ThreadedContourGenerator",
    "ZInterp",
]


def _name_to_class(name):
    class_name = f"{name.capitalize()}ContourGenerator"
    cls = globals()[class_name]
    return cls


def contour_generator(x, y, z, name=None, corner_mask=None, chunk_size=None, line_type=None,
                      fill_type=None, quad_as_tri=None, z_interp=ZInterp.Linear, chunk_count=None,
                      total_chunk_count=None, thread_count=0):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.ma.asarray(z, dtype=np.float64)  # Preserve mask if present.

    # Check arguments: z.
    if z.ndim != 2:
        raise TypeError(f"Input z must be 2D, not {z.ndim}D")
    if z.shape[0] < 2 or z.shape[1] < 2:
        raise TypeError(f"Input z must be at least a (2, 2) shaped array, but has shape {z.shape}")

    ny, nx = z.shape

    # Check arguments: x and y.
    if x.ndim != y.ndim:
        raise TypeError(f"Number of dimensions of x ({x.ndim}) and y ({y.ndim}) do not match")
    if x.ndim == 0:
        x = np.arange(nx)
        y = np.arange(ny)
        x, y = np.meshgrid(x, y)
    elif x.ndim == 1:
        if len(x) != nx:
            raise TypeError(f"Length of x ({len(x)}) must match number of columns in z ({nx})")
        if len(y) != ny:
            raise TypeError(f"Length of y ({len(y)}) must match number of rows in z ({ny})")
        x, y = np.meshgrid(x, y)
    elif x.ndim == 2:
        if x.shape != z.shape:
            raise TypeError(f"Shapes of x {x.shape} and z {z.shape} do not match")
        if y.shape != z.shape:
            raise TypeError(f"Shapes of y {y.shape} and z {z.shape} do not match")
    else:
        raise TypeError(f"Inputs x and y must be None, 1D or 2D, not {x.ndim}D")

    # Extract optional mask from z array.
    mask = None
    if np.ma.is_masked(z):
        mask = np.ma.getmask(z)
        if mask is np.ma.nomask:
            mask = None
        z = np.ma.getdata(z)

    # Check mask shape just in case.
    if mask is not None and mask.shape != z.shape:
        raise ValueError("If mask is set it must be a 2D array with the same shape as z")

    # Check arguments: name.
    if name is None:
        name = "serial"  # Default algorithm.

    if name not in ("mpl2005", "mpl2014", "serial", "threaded"):
        raise ValueError(f"Unrecognised contour generator name: {name}")

    # Check arguments: chunk_size, chunk_count and total_chunk_count.
    y_chunk_size, x_chunk_size = calc_chunk_sizes(
        chunk_size, chunk_count, total_chunk_count, ny, nx)

    cls = _name_to_class(name)

    # Check arguments: corner_mask.
    if corner_mask is None:
        # Set it to default, which is True if the algorithm supports it.
        corner_mask = cls.supports_corner_mask()
    elif corner_mask and not cls.supports_corner_mask():
        raise ValueError(f"{name} contour generator does not support corner_mask=True")

    # Check arguments: line_type.
    if line_type is None:
        line_type = cls.default_line_type
    if not cls.supports_line_type(line_type):
        raise ValueError(f"{name} contour generator does not support line_type {line_type}")

    # Check arguments: fill_type.
    if fill_type is None:
        fill_type = cls.default_fill_type
    if not cls.supports_fill_type(fill_type):
        raise ValueError(f"{name} contour generator does not support fill_type {fill_type}")

    # Check arguments: quad_as_tri.
    if quad_as_tri is None:
        quad_as_tri = False  # Default.
    elif quad_as_tri and not cls.supports_quad_as_tri():
        raise ValueError(f"{name} contour generator does not support quad_as_tri=True")

    # Check arguments: z_interp.
    if z_interp != ZInterp.Linear and not cls.supports_z_interp():
        raise ValueError(f"{name} contour generator does not support z_interp {z_interp}")

    # Check arguments: thread_count.
    if thread_count not in (0, 1) and not cls.supports_threads():
        raise ValueError(f"{name} contour generator does not support thread_count {thread_count}")

    # Prepare args and kwargs for contour generator constructor.
    args = [x, y, z, mask]
    kwargs = {
        "x_chunk_size": x_chunk_size,
        "y_chunk_size": y_chunk_size,
    }

    if name not in ("mpl2005", "mpl2014"):
        kwargs["line_type"] = line_type
        kwargs["fill_type"] = fill_type
    if cls.supports_corner_mask():
        kwargs["corner_mask"] = corner_mask
    if cls.supports_quad_as_tri():
        kwargs["quad_as_tri"] = quad_as_tri
    if cls.supports_z_interp():
        kwargs["z_interp"] = z_interp
    if cls.supports_threads():
        kwargs["thread_count"] = thread_count

    # Create contour generator.
    cont_gen = cls(*args, **kwargs)

    return cont_gen
