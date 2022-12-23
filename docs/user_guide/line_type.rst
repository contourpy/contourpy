.. _line_type:

Line type
---------

:class:`~contourpy.LineType` is an enum that is passed as the ``line_type`` keyword argument to
:func:`~contourpy.contour_generator()` and is used to specify the format of data returned from calls
to :func:`~contourpy.ContourGenerator.lines`. If not explicitly specified then the default is
used for the requested algorithm ``name``.

Supported enum members and the default vary by algorithm:

.. name_supports_type:: LineType

A string name can be used instead of the enum member so the following are equivalent:

   >>> contour_generator(line_type="SeparateCode", ...)
   >>> contour_generator(line_type=LineType.SeparateCode, ...)

Enum members are a combination of the following words:

- **Separate**: each line is a separate array.
- **Combined**: multiple lines are concatenated in the same array.
- **Chunk**: each chunk is separate, and is ``None`` if the chunk has no lines.
- **Code**: includes `Matplotlib`_ kind codes for the previous line array.
- **Offset**: individual lines are identified via offsets into the previous line array.

The format of data returned by :func:`~contourpy.ContourGenerator.lines` for each of the
possible :class:`~contourpy.LineType` members is best illustrated through an example.

.. plot::
   :separate-modes:
   :source-position: none

   from contourpy import contour_generator
   from contourpy.util.mpl_renderer import MplDebugRenderer as Renderer
   import numpy as np

   renderer = Renderer(figsize=(4, 2.8))
   x = np.arange(4)
   y = np.arange(3)
   z = [[1.4, 1.2, 0.9, 0], [0.6, 3, 0.4, 0.7], [0.2, 0.2, 0.5, 3]]
   cont_gen = contour_generator(x, y, z)
   lines = cont_gen.lines(2)
   c = 'C0'
   renderer.lines(lines, cont_gen.line_type, linewidth=2, color=c, start_point_color=c)
   renderer.grid(x, y, color="gray", alpha=0.2)
   renderer.z_values(x, y, z, color="C2")
   renderer.title("Contour lines at z=2")
   renderer.show()

For the ``z`` values shown in green text, two contour lines are returned at ``z=2``:

- A closed line loop that is entirely within the domain and consists of 5 points, the last point is
  the same as the first.
- An open line strip that starts and ends on boundaries of the domain and consists of 2 points.

.. note::

   Contour line segments are directed with higher ``z`` on the left, hence closed line loops are
   oriented anticlockwise if they enclose a region that is higher then the contour level, or
   clockwise if they enclose a region that is lower than the contour level.  This assumes a
   right-hand coordinate system.

First set up the imports, define the ``z`` array and limit `NumPy`_ printing to 2 decimal places:

   >>> from contourpy import contour_generator, LineType
   >>> import numpy as np
   >>> np.set_printoptions(precision=2)
   >>> z = [[1.4, 1.2, 0.9, 0], [0.6, 3, 0.4, 0.7], [0.2, 0.2, 0.5, 3]]

Separate
^^^^^^^^
   >>> cont_gen = contour_generator(z=z, line_type=LineType.Separate)
   >>> lines = cont_gen.lines(2)
   >>> lines
   [array([[0.58, 1.], [1., 0.44], [1.38, 1.], [1., 1.36], [0.58, 1.]]),
    array([[2.6, 2.], [3., 1.57]])]

This returns a list of arrays, each array is the 2D points of a single line loop or strip.
The number of lines is ``len(lines)`` and the points of line ``i`` are ``lines[i]``.

SeparateCode
^^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, line_type=LineType.SeparateCode)
   >>> lines = cont_gen.lines(2)
   >>> lines
   ([array([[0.58, 1.], [1., 0.44], [1.38, 1.], [1., 1.36], [0.58, 1.]]),
     array([[2.6, 2.], [3., 1.57]])],
    [array([1, 2, 2, 2, 79], dtype=uint8),
     array([1, 2], dtype=uint8)])

This returns a tuple of two lists, each list has a length equal to the number of lines.
The first list is the same as for ``LineType.Separate``. The second list is of 1D ``np.uint8``
arrays containing the `Matplotlib`_ kind codes (1 = start new line loop or strip, 2 = move to
point, 79 = close line loop). For line ``i`` the points are ``lines[0][i]`` and the kind codes are
``lines[1][i]``.

ChunkCombinedCode
^^^^^^^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, line_type=LineType.ChunkCombinedCode)
   >>> lines = cont_gen.lines(2)
   >>> lines
   ([array([[0.58, 1.], [1., 0.44], [1.38, 1.], [1., 1.36], [0.58, 1.], [2.6, 2.], [3., 1.57]])],
    [array([1, 2, 2, 2, 79, 1, 2], dtype=uint8)])

This returns a tuple of two lists, each list has a length equal to the number of chunks used which
is one here. The first list contains a 2D ``np.float64`` array for each chunk containing the
combined points for all lines in that chunk, and the second list contains a 1D ``np.uint8`` array
for each chunk containing the combined `Matplotlib`_ kind codes for all lines in that chunk.

For chunk ``j`` the combined points are ``lines[0][j]`` and the combined codes are ``lines[1][j]``.
An empty chunk has ``None`` for each. The start of each line loop/strip is identified by a kind code
of 1.

ChunkCombinedOffset
^^^^^^^^^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, line_type=LineType.ChunkCombinedOffset)
   >>> lines = cont_gen.lines(2)
   >>> lines
   ([array([[0.58, 1.], [1., 0.44], [1.38, 1.], [1., 1.36], [0.58, 1.], [2.6, 2.], [3., 1.57]])],
    [array([0, 5, 7], dtype=uint32)])

This returns a tuple of two lists, each list has a length equal to the number of chunks used which
is one here. The first list contains a 2D ``np.float64`` array for each chunk containing the
combined points for all lines in that chunk, and the second list contains a 1D ``np.uint32`` array
for each chunk containing the start and end offsets of lines in that chunk's point array.

For chunk ``j`` the combined points are ``lines[0][j]`` and the combined offsets are
``lines[1][j]``. An empty chunk has ``None`` for each. In this example the first line corresponds
to point indices ``0:5`` and the second to ``5:7``. The length of the offset array is one more than
the number of lines.

How to choose which line type to use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Do you need `Matplotlib`_ kind codes?

#. Do you want each line's points in a separate array or combined together?

The second question is one of convenience and performance. It is often more convenient to deal with
a single array of points per line, but it is slower to do this as more arrays have to be created.
The difference may only be significant for scenarios that generate many contour lines.
See :ref:`benchmarks`.

The decision also depends on how the line data is to be used. The performance advantage of combined
arrays is usually wasted if the lines have to separated out into their own arrays for subsequent
analysis.

.. note::

   The order of lines returned by a particular :func:`~contourpy.ContourGenerator.lines` call
   is deterministic except for the combination of ``name="threaded"`` and either
   ``line_type=LineType.Separate`` or ``line_type=LineType.SeparateCode``. This is because the
   order that the chunks are processed in is not deterministic and lines are appended to the
   returned arrays as soon as their chunks are completed.
