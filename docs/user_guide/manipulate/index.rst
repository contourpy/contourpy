Manipulate contours
===================

The format of contour data returned by :meth:`~.ContourGenerator.lines`,
:meth:`~.ContourGenerator.filled`, :meth:`~.ContourGenerator.multi_lines` and
:meth:`~.ContourGenerator.multi_filled` is controlled by the ``line_type``, ``fill_type`` and
chunking keyword arguments passed to :func:`~.contour_generator`. Usually this is fully
within your control but there may be occasions when it is not, such as when your contour data is
obtained via a third-party library that limits some of the available options. ContourPy includes
functions to manipulate contour data that has been returned to you in such situations.

.. toctree::
   :maxdepth: 1

   convert
   dechunk
