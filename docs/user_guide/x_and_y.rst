x and y grid
============

``x`` and ``y`` are optional keyword arguments to :func:`~contourpy.contour_generator` that are
used to specify the (x, y) grid that the ``z`` values are located on. They may be 1D or 2D `NumPy`_
arrays of ``np.float64`` or convertible to such. If one is specified then so should the other, and
they must both have the same number of dimensions.

If the ``z`` array has shape ``(ny, nx)`` then the options available for ``x`` and ``y`` are:

#. Both 2D of shape ``(ny, nx)``.

#. Both 1D with ``x.shape = (nx,)`` and ``y.shape = (ny,)``.  These are broadcast from 1D to 2D in
   :func:`~contourpy.contour_generator` using ``x, y = np.meshgrid(x, y)``.

#. Both ``None``, in which case :func:`~contourpy.contour_generator` uses
   ``x = np.arange(nx, dtype=np.float64)`` and ``y = np.arange(ny, dtype=np.float64)`` and then
   broadcasts them to 2D as above.

.. warning::

   ``contourpy`` assumes that the ``x`` and ``y`` values are reasonable and does not check that they
   are.  They should be monotonic.  They should not contain non-finite values like ``np.inf`` or
   ``np.nan``.  If they are masked arrays then the masks are ignored.

.. note::

   To mask out grid points the mask must be applied to the ``z`` array, not the ``x`` or ``y``
   arrays. See :ref:`z mask <z_mask>`.

Individual quads should be either convex or 3-point collinear.  Concave quads may produce
acceptable results in some situations but not others so they should be avoided.

.. plot::
   :separate-modes:
   :source-position: none

   from contourpy.util.mpl_renderer import MplRenderer as Renderer

   renderer = Renderer(ncols=3, figsize=(5, 1.6), show_frame=False)

   x = [[0, 1], [0, 1]]
   y = [[0, 0], [1, 1]]
   renderer.grid(x, y, ax=0, alpha=1, color="green", point_color="green")
   renderer.title("Convex: OK", ax=0, color="green")

   x[0][1] = y[0][1] = 0.5
   renderer.grid(x, y, ax=1, alpha=1, color="green", point_color="green")
   renderer.title("Collinear: OK", ax=1, color="green")

   x[0][1] = 0.4
   y[0][1] = 0.6
   renderer.grid(x, y, ax=2, alpha=1, color="red", point_color="red")
   renderer.title("Concave: not OK", ax=2, color="red")

   renderer.show()

.. note::

   ``quad_as_tri=True`` is more tolerant of concave quads. Provided the central virtual point
   (mean x, y of the corner points) lies within the quad then it will be contoured correctly.

Most of the examples in this documentation use Cartesian grids. But they do not have to be, here are
examples of curved and polar grids:

.. plot::
   :separate-modes:
   :source-position: below

   from contourpy.util.mpl_renderer import MplRenderer as Renderer
   import numpy as np

   renderer = Renderer(ncols=2, figsize=(6, 3))

   i = np.linspace(-0.7, 0.7, 10)
   j = np.linspace(-0.7, 0.7, 10)
   i, j = np.meshgrid(i, j)
   x = i + 0.4*i*j - 0.2*j*j
   y = j - 0.3*i*i + 0.5*i*j
   renderer.grid(x, y, ax=0, color="gray", alpha=1)

   radius, theta = np.meshgrid(np.linspace(0, 1, 4), np.linspace(0, 2*np.pi, 25))
   x = radius*np.cos(theta)
   y = radius*np.sin(theta)
   renderer.grid(x, y, ax=1, color="gray", alpha=1)

   renderer.show()

.. warning::

   If ``x`` or ``y`` are 2D contiguous C-ordered ``np.float64`` arrays then they are not copied by
   :func:`~contourpy.contour_generator` and they can be altered in your client code after the
   :class:`~contourpy.ContourGenerator` has been created.  See :ref:`z_array` for more details.
