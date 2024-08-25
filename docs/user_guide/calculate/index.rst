Calculate contours
==================

Contours are calculated using the :meth:`~.ContourGenerator.lines`,
:meth:`~.ContourGenerator.filled`, :meth:`~.ContourGenerator.multi_lines` and
:meth:`~.ContourGenerator.multi_filled` methods of a :class:`~.ContourGenerator` object
that is obtained by calling the :func:`~.contour_generator` function.
There are many options available for contouring that equate to keyword arguments passed to
the :func:`~.contour_generator` function, these are described in turn below.

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
   limitations
