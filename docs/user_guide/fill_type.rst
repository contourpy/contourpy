.. _fill_type:

Fill type
---------

:class:`~contourpy.FillType` is an enum that is passed as the ``fill_type`` keyword argument to
:func:`~contourpy.contour_generator()` and is used to specify the format of data returned from calls
to :func:`~contourpy.ContourGenerator.filled`. If not explicitly specified then the default is
used for the requested algorithm ``name``.

Supported enum members and the default vary by algorithm:

.. name_supports_type:: FillType

A string name can be used instead of the enum member so the following are equivalent:

   >>> contour_generator(fill_type="OuterOffset", ...)
   >>> contour_generator(fill_type=FillType.OuterOffset, ...)

.. note::

   Filled contours are more complicated than contour lines because lines are independent of each
   other whereas filled contours consist of polygons that always have an outer (exterior) boundary
   but may also contain any number of holes (interior boundaries). The relationship between outer
   boundaries and their holes is calculated and returned by
   :func:`~contourpy.ContourGenerator.filled` for all :class:`~contourpy.FillType` members
   except for ``ChunkCombinedCode`` and ``ChunkCombinedOffset``.

Enum members are a combination of the following words:

- **Outer**: each outer boundary is stored with its holes in a separate array to other outer
  boundaries.
- **Combined**: multiple boundaries are concatenated in the same array regardless of whether they
  are outer boundaries or holes.
- **Chunk**: each chunk is separate, and is ``None`` if the chunk has no polygons.
- **Code**: includes `Matplotlib`_ kind codes for the previous array.
- **Offset**: the previous array is divided up using start and end offsets.

Where **Offset** occurs twice the first refers to the offsets of individual boundaries (outers and
holes) within a larger collection and the second to which of those boundaries are grouped together
into polygons.

The format of data returned by :func:`~contourpy.ContourGenerator.filled` for each of the
possible :class:`~contourpy.FillType` members is best illustrated through an example.  This is the
same example data used for :ref:`line_type` but calling ``filled(1, 2)`` instead of ``lines(2)``.

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
   filled = cont_gen.filled(1, 2)
   c = 'C0'
   renderer.filled(filled, cont_gen.fill_type, color=c, point_color=c, start_point_color=c,
      line_color=c, alpha=0.3, line_alpha=1.0)
   renderer.grid(x, y, color="gray", alpha=0.2)
   renderer.z_values(x, y, z, color="C2")
   renderer.title("Filled contours between z=1 and 2")
   renderer.show()

This example returns two polygons:

- A polygon that has an outer (exterior boundary) and one hole (interior boundary). The outer has
  8 points (first and last are identical) that are on either the lower contour level or the domain
  boundary, the hole has 5 points (first and last are identical) all on the upper contour level.
- A simple polygon without any holes consisting of 5 points (first and last are identical) that
  follows the lower contour level, then the domain boundary, then the upper contour level and the
  domain boundary again.

.. note::

   Outer boundaries are oriented in an anticlockwise manner, holes are oriented clockwise.
   This assumes a right-hand coordinate system.

Set up the imports and data:

   >>> from contourpy import contour_generator, FillType
   >>> import numpy as np
   >>> np.set_printoptions(precision=2)
   >>> z = [[1.4, 1.2, 0.9, 0], [0.6, 3, 0.4, 0.7], [0.2, 0.2, 0.5, 3]]

OuterCode
^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, fill_type=FillType.OuterCode)
   >>> filled = cont_gen.filled(1, 2)
   >>> filled
   ([array([[0., 0.], [1., 0.], [1.67, 0.], [1.77, 1.], [1., 1.71], [0.17, 1.], [0., 0.5],
            [0., 0.], [1., 0.44], [0.58, 1.], [1., 1.36], [1.38, 1.], [1., 0.44]]),
     array([[2.2 , 2.], [3., 1.13], [3., 1.57], [2.6, 2.], [2.2, 2.]])],
    [array([1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79], dtype=uint8),
     array([1, 2, 2, 2, 79], dtype=uint8)])

This returns a tuple of two lists, each list has a length equal to the number of polygons. Each
polygon comprises an outer boundary and its holes. The first list contains the polygons points and
the second list their corresponding `Matplotlib`_ kind codes. For polygon ``i`` the points are
``filled[0][i]`` and the ``matplotlib`` kind codes are ``filled[1][i]``.

Here the first polygon has 13 points, 8 for the outer and 5 for the hole. The hole starts at index
8 which corresponds to a kind code of 1.

OuterOffset
^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, fill_type=FillType.OuterOffset)
   >>> filled = cont_gen.filled(1, 2)
   >>> filled
   ([array([[0., 0.], [1., 0.], [1.67, 0.], [1.77, 1.], [1., 1.71], [0.17, 1.], [0., 0.5],
            [0., 0.], [1., 0.44], [0.58, 1.], [1., 1.36], [1.38, 1.], [1., 0.44]]),
     array([[2.2 , 2.], [3., 1.13], [3., 1.57], [2.6, 2.], [2.2, 2.]])],
    [array([0, 8, 13], dtype=uint32),
     array([0, 5], dtype=uint32)])

This returns a tuple of two lists, each list has a length equal to the number of polygons. Each
polygon comprises an outer boundary and its holes. The first list contains the polygons points and
the second list the offsets into the points arrays for the start and end indices of the outers and
holes. For polygon ``i`` the points are ``filled[0][i]`` and offsets are ``filled[1][i]``.

Here the first polygon has 13 points, the outer is indices ``0:8`` and the hole is indices
``8:13``. The second polygon does not have any holes so its indices ``0:5`` cover the whole of its
points array.

ChunkCombinedCode
^^^^^^^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, fill_type=FillType.ChunkCombinedCode)
   >>> filled = cont_gen.filled(1, 2)
   >>> filled
   ([array([[0., 0.], [1., 0.], [1.67, 0.], [1.77, 1.], [1., 1.71], [0.17, 1.], [0., 0.5],
            [0., 0.], [1., 0.44], [0.58, 1.], [1., 1.36], [1.38, 1.], [1., 0.44], [2.2 , 2.],
            [3., 1.13], [3., 1.57], [2.6, 2.], [2.2, 2.]])],
    [array([1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79, 1, 2, 2, 2, 79], dtype=uint8)])

This returns a tuple of two lists, each list has a length equal to the number of chunks used which
is one here. All of the boundary points are combined into a single array per chunk, there is no
information on the relationship between the outer boundaries and their holes, and each outer is not
necessarily stored contiguously with its corresponding holes. The first list contains the boundary
points and the second list their corresponding `Matplotlib`_ kind codes.

For chunk ``j`` the combined points are ``filled[0][j]`` and the combined codes are
``filled[1][j]``. An empty chunk has ``None`` for each. The start of each polygon boundary is
identified by a kind code of 1, so here there are three boundaries.

ChunkCombinedOffset
^^^^^^^^^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, fill_type=FillType.ChunkCombinedOffset)
   >>> filled = cont_gen.filled(1, 2)
   >>> filled
   ([array([[0., 0.], [1., 0.], [1.67, 0.], [1.77, 1.], [1., 1.71], [0.17, 1.], [0., 0.5],
            [0., 0.], [1., 0.44], [0.58, 1.], [1., 1.36], [1.38, 1.], [1., 0.44], [2.2 , 2.],
            [3., 1.13], [3., 1.57], [2.6, 2.], [2.2, 2.]])],
    [array([0, 8, 13, 18], dtype=uint32)])

This returns a tuple of two lists, each list has a length equal to the number of chunks used which
is one here. All of the boundary points are combined into a single array per chunk, there is no
information on the relationship between the outer boundaries and their holes, and each outer is not
necessarily stored contiguously with its corresponding holes. The first list contains the boundary
points and the second list the offsets in the points array of the boundary starts and ends.

For chunk ``j`` the combined points are ``filled[0][j]`` and the combined offsets` are
``filled[1][j]``. An empty chunk has ``None`` for each. Here there are three boundaries
with point indices ``0:8``, ``8:13`` and ``13:18`` respectively.

ChunkCombinedCodeOffset
^^^^^^^^^^^^^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, fill_type=FillType.ChunkCombinedCodeOffset)
   >>> filled = cont_gen.filled(1, 2)
   >>> filled
   ([array([[0., 0.], [1., 0.], [1.67, 0.], [1.77, 1.], [1., 1.71], [0.17, 1.], [0., 0.5],
            [0., 0.], [1., 0.44], [0.58, 1.], [1., 1.36], [1.38, 1.], [1., 0.44], [2.2 , 2.],
            [3., 1.13], [3., 1.57], [2.6, 2.], [2.2, 2.]])],
    [array([1, 2, 2, 2, 2, 2, 2, 79, 1, 2, 2, 2, 79, 1, 2, 2, 2, 79], dtype=uint8)],
    [array([ 0, 13, 18], dtype=uint32)])

This returns a tuple of three lists, each list has a length equal to the number of chunks used
which is one here. The first two lists are the same as for ``ChunkCombinedCode`` except that each
outer and its holes are stored contiguously. The third list is an array of offsets into the points
and codes arrays to identify the start and end indices of each polygon (outer with its holes) within
those arrays.

For chunk ``j`` the combined points are ``filled[0][j]``, the combined codes are ``filled[1][j]``
and the combined polygon offsets are ``filled[2][j]``. An empty chunk has ``None`` for all three.

Here there are 18 points in three boundaries, the latter starting at indices 0, 8 and 13 which are
determined from the kind codes of 1. The polygon offsets arrays indicates that there are two
polygons, the first is indices ``0:13`` (so outer plus one hole) and the second is indices ``13:18``
(outer only).

ChunkCombinedOffsetOffset
^^^^^^^^^^^^^^^^^^^^^^^^^
   >>> cont_gen = contour_generator(z=z, fill_type=FillType.ChunkCombinedOffsetOffset)
   >>> filled = cont_gen.filled(1, 2)
   >>> filled
   ([array([[0., 0.], [1., 0.], [1.67, 0.], [1.77, 1.], [1., 1.71], [0.17, 1.], [0., 0.5],
            [0., 0.], [1., 0.44], [0.58, 1.], [1., 1.36], [1.38, 1.], [1., 0.44], [2.2 , 2.],
            [3., 1.13], [3., 1.57], [2.6, 2.], [2.2, 2.]])],
    [array([ 0,  8, 13, 18], dtype=uint32)],
    [array([0, 2, 3], dtype=uint32)])

This returns a tuple of three lists, each list has a length equal to the number of chunks used
which is one here. The first two lists are the same as for ``ChunkCombinedOffset`` except that each
outer and its holes are stored contiguously. The third list is an array of polygon offsets into the
boundary offsets array to identify the start and end indices of each polygon.

For chunk ``j`` the combined points are ``filled[0][j]``, the combined boundary offsets are
``filled[1][j]`` and the combined polygon offsets are ``filled[2][j]``. An empty chunk has ``None``
for all three.

Here there are three boundaries with point indices ``0:8``, ``8:13`` and ``13:18`` respectively,
and two polygons with boundary indices ``0:2`` and ``2:3`` respectively. So the first polygon
consists of two boundaries (outer plus one hole) and the second polygon is a single boundary (outer
only).

How to choose which fill type to use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Do you need `Matplotlib`_ kind codes?

#. Do you want each boundary's points in a separate array or combined together?

#. Do you want each outer boundary and its corresponding holes to be grouped together?

As with contour lines, the second question is one of convenience and performance. It is often more
convenient to deal with a single array of points per polygon, but it is slower to do this as more
arrays have to be created.  The difference may only be significant for scenarios that generate many
polygons.  See :ref:`benchmarks`.

The decision also depends on how the polygon data is to be used. The performance advantage of
combined arrays is usually wasted if the polygons have to separated out into their own arrays for
subsequent analysis.

.. note::

   The order of boundaries returned by a particular :func:`~contourpy.ContourGenerator.filled`
   call is deterministic except for the combination of ``name="threaded"`` and either
   ``fill_type=FillType.OuterCode`` or ``fill_type=FillType.OuterOffset``. This is because the
   order that the chunks are processed in is not deterministic and boundaries are appended to the
   returned arrays as soon as their chunks are completed.
