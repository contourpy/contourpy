.. _z_interp:

z interpolation
---------------

Interpolation of ``z`` values occurs in two situations:

#. When calculating how far along the edge of a quad (or corner-masked corner) a contour line
   intersects it.

#. When calculating the ``z`` value of the central point of quad. This is needed for all quads if
   ``quad_as_tri=True`` or just saddle quads if ``quad_as_tri=False`` (see
   :ref:`algorithm_description` about saddle quads).

The default for all algorithms is linear z-interpolation, but ``serial`` and ``threaded`` support
the use of a :class:`~contourpy.ZInterp` enum that contains other possibilities.

.. name_supports::
   :filter: z_interp

.. note::

   Currently the only members of :class:`~contourpy.ZInterp` are ``ZInterp.Linear`` and
   ``ZInterp.Log``.

To use alternative z-interpolation, pass the ``z_interp`` keyword argument to
:func:`~contourpy.contour_generator`. A string name can be used instead of the enum member so the
following are equivalent:

   >>> contour_generator(z_interp="Log", ...)
   >>> contour_generator(z_interp=ZInterp.Log, ...)

.. warning:

   If you are using logarithmic z-interpolation, all unmasked ``z`` values must be positive.

When might logarithmic z-interpolation be appropriate?  When contour levels are exponentially
distributed, as exponential and logarithm are inverse transforms.

The example below has a coarse rotated grid where ``z = np.exp(6*y)`` and the contour levels
``[0.3, 1, 3, 10, 30, 100]`` increase exponentially. Using linear z-interpolation the contour lines
are jagged, using logarithmic z-interpolation the contour lines are straight and at constant ``y``,
as expected.

.. plot::
   :separate-modes:
   :source-position: below

   from contourpy import contour_generator, ZInterp
   from contourpy.util.mpl_renderer import MplRenderer as Renderer
   import numpy as np

   n = 4
   angle = 0.4  # Radians.

   # Rotated grid.
   x, y = np.meshgrid(np.linspace(0.0, 1.0, n), np.linspace(0.0, 1.0, n))
   rot = [[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]]
   x, y = np.einsum('ji,mni->jmn', rot, np.dstack([x, y]))

   # z is exponential in y.
   z = np.exp(6*y)
   levels = [0.3, 1, 3, 10, 30, 100]

   renderer = Renderer(ncols=2, figsize=(8, 4))

   for ax, z_interp in enumerate([ZInterp.Linear, ZInterp.Log]):
      renderer.grid(x, y, ax=ax, color="gray", alpha=0.2)
      cont_gen = contour_generator(x, y, z, z_interp=z_interp)
      for i, level in enumerate(levels):
          lines = cont_gen.lines(level)
          renderer.lines(lines, cont_gen.line_type, ax=ax, color=f"C{i}", linewidth=2)
      renderer.z_values(x, y, z, ax=ax)
      renderer.title(z_interp, ax=ax)

   renderer.show()

.. note::

   The difference is much less pronounced on a finer (higher resolution) grid, which can be
   confirmed by increasing the grid resolution ``n``.
