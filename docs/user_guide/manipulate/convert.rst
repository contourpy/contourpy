Convert line and fill types
---------------------------

Convert contour lines to a different line type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`~.convert_lines` and :func:`~.convert_multi_lines` are used to convert contour lines to a
different :class:`~.LineType`.

The following example creates two contour lines in ``LineType.Separate`` format where each line's 2D
points are in separate NumPy arrays:

   >>> from contourpy import contour_generator, convert_lines
   >>> cont_gen = contour_generator(z=[[0, 1, 0], [0, 1, 0]], line_type="Separate")
   >>> lines = cont_gen.lines(0.5)
   >>> lines
   [array([[0.5, 1.], [0.5, 0.]]), array([[1.5, 0.], [1.5, 1.]])]

This can be converted to ``LineType.ChunkCombinedOffset``:

   >>> lines = convert_lines(lines, cont_gen.line_type, "ChunkCombinedOffset")
   >>> lines
   ([array([[0.5, 1.], [0.5, 0.], [1.5, 0.], [1.5, 1.]])], [array([0, 2, 4], dtype=uint32)])

in which the lines are combined into a single array of 2D points and the offset array shows the
start and end offsets of each line.

Any :class:`~.LineType` can be converted to any other :class:`~.LineType`.
When converting from a non-chunked line type (``LineType.Separate`` or ``LineType.SeparateCode``) to
a chunked one (``LineType.ChunkCombinedCode``, ``LineType.ChunkCombinedOffset`` or
``LineType.ChunkCombinedNan``), all lines are placed together in the first chunk. When converting in
the other direction, all chunk information is discarded as all lines are appended to the same list
(``LineType.Separate``) or lists (``LineType.SeparateCode``).

Convert filled contours to a different fill type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`~.convert_filled` and :func:`~.convert_multi_filled` are used to convert filled contours to a
different :class:`~.FillType`.

The following example creates two filled polygons in ``FillType.OuterCode`` format where each of the
polygons points and codes are in separate NumPy arrays:

   >>> from contourpy import contour_generator, convert_filled
   >>> cont_gen = contour_generator(z=[[0, 1, 0], [0, 1, 0]], fill_type="OuterCode")
   >>> filled = cont_gen.filled(0.3, 0.6)
   >>> filled
   ([array([[0.3, 0.], [0.6, 0.], [0.6, 1.], [0.3, 1.], [0.3, 0.]]),
     array([[1.4, 0.], [1.7, 0.], [1.7, 1.], [1.4, 1.], [1.4, 0.]])],
    [array([1, 2, 2, 2, 79], dtype=uint8),
     array([1, 2, 2, 2, 79], dtype=uint8)])

This can be converted to ``FillType.ChunkCombinedOffsetOffset``:

   >>> filled = convert_filled(filled, cont_gen.fill_type, "ChunkCombinedOffsetOffset")
   >>> filled
   ([array([[0.3, 0.], [0.6, 0.], [0.6, 1.], [0.3, 1.], [0.3, 0.],
            [1.4, 0.], [1.7, 0.], [1.7, 1.], [1.4, 1.], [1.4, 0.]])],
    [array([0, 5, 10], dtype=uint32)],
    [array([0, 1, 2], dtype=uint32)])

in which the points are combined into a single 2D array and there are two arrays of offsets, one
for the boundary offsets and one for the polygon (outer boundary) offsets.

Not all :class:`~.FillType` can be converted to any other :class:`~.FillType`.
Two of the :class:`~.FillType` (``FillType.ChunkCombinedCode`` and
``FillType.ChunkCombinedOffset``) do not include information about the relationship between outer
and inner boundaries so they cannot be converted to any of the :class:`~.FillType` that
need this information (``FillType.OuterCode``, ``FillType.OuterOffset``,
``FillType.ChunkCombinedCodeOffset`` and ``FillType.ChunkCombinedOffsetOffset``);
a ``ValueError`` will be raised instead.

Also, when converting from a non-chunked fill type (``FillType.OuterCode`` or
``FillType.OuterOffset``) to a chunked one (any of the others), all polygons are placed together in
the first chunk. When converting in the other direction, all chunk information is discarded as all
polygons are appended to the same lists.
