.. _quad_as_tri:

Quad as triangles
-----------------

A contour line within a quad is, by default, a straight line between points on two of its edges.
The ``quad_as_tri`` option divides each quad into four triangles using a virtual point at the
centre (mean x, y of the corner points) and extra contour points are inserted where the contour
level intersects the diagonals so that contour lines are piecewise linear within the triangles.

The ``z`` value of the central point is calculated depending on the :ref:`z_interp` setting; for
the default ``z_interp=ZInterp.Linear`` this is the mean of the ``z`` values of the corner points.
Corner masked triangles are not affected by this setting, only full unmasked quads.

.. name_supports::
   :filter: quad_as_tri

``quad_as_tri`` is available for the ``serial`` and ``threaded`` algorithms.  It is always disabled
by default, so if required it must be explicitly requested:

  >>> cont_gen = contour_generator(quad_as_tri=True, ...)

.. note::

   ``quad_as_tri`` produces more detailed contours, but not necessarily smoother ones.

Here is an example of the difference between ``quad_as_tri=False`` and ``True`` for ``z`` values on
a coarse grid that are given by ``z = np.sqrt(x**2 + y**2)``. On a finer grid the contours would be
semicircular.

.. plot::
   :separate-modes:
   :source-position: below

   from contourpy import contour_generator
   from contourpy.util.mpl_renderer import MplRenderer as Renderer
   import numpy as np

   x, y = np.meshgrid([-2, -1, 0, 1, 2], [0, 1, 2])
   z = np.sqrt(x**2 + y**2)

   renderer = Renderer(ncols=2, figsize=(8, 2.4))
   for ax in range(2):
      quad_as_tri = bool(ax)
      renderer.grid(x, y, ax=ax, color="gray", alpha=0.2, quad_as_tri_alpha=ax*0.1)
      renderer.title(f"quad_as_tri={quad_as_tri}", ax=ax)

      cont_gen = contour_generator(x, y, z, quad_as_tri=quad_as_tri)
      for i, level in enumerate(np.arange(0.5, 2.51, 0.5)):
         lines = cont_gen.lines(level)
         renderer.lines(lines, cont_gen.line_type, ax=ax, color=f"C{i}", linewidth=2)

      renderer.z_values(x, y, z, ax=ax, quad_as_tri=quad_as_tri, fmt="0.2f")

   renderer.show()

Another situation in which ``quad_as_tri`` may be useful is shown below. The quad has three corners
at the same ``z`` level so without ``quad_as_tri`` contour lines cut across diagonally.

.. plot::
   :separate-modes:
   :source-position: below

   from contourpy import contour_generator
   from contourpy.util.mpl_renderer import MplRenderer as Renderer
   import numpy as np

   x = y = [0, 1]
   z = [[0, 0], [0, 4]]

   renderer = Renderer(ncols=2, figsize=(6, 3))
   for ax in range(2):
      quad_as_tri = bool(ax)
      renderer.grid(x, y, ax=ax, color="gray", alpha=0.2, quad_as_tri_alpha=ax*0.1)
      renderer.title(f"quad_as_tri={quad_as_tri}", ax=ax)

      cont_gen = contour_generator(x, y, z, quad_as_tri=quad_as_tri)
      for i, level in enumerate(np.arange(0.0, 4.0, 0.4)):
         lines = cont_gen.lines(level)
         renderer.lines(lines, cont_gen.line_type, ax=ax, color=f"C{i}", linewidth=2)

      renderer.z_values(x, y, z, ax=ax, quad_as_tri=quad_as_tri)

   renderer.show()

.. note::

   ``quad_as_tri=True`` produces contour lines and filled contours typically containing about three
   times as many points as ``quad_as_tri=False``.
