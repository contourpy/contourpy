Calculate contours
==================

Contours are calculated using the :meth:`~contourpy.ContourGenerator.lines` and
:meth:`~contourpy.ContourGenerator.filled` methods of a :class:`~contourpy.ContourGenerator` object
that is obtained by calling the :func:`~contourpy.contour_generator` function.
There are many options available for contouring that equate to keyword arguments passed to
the :func:`~contourpy.contour_generator` function.

Before reading this you should check out the :ref:`quickstart`.

The other main source of information is the :ref:`api`.

.. toctree::
   :maxdepth: 1

   name
   z_corner_mask
   x_and_y
   chunks
   line_type
   fill_type
   quad_as_tri
   z_interp
   threads
