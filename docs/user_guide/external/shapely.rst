Shapely
=======

`Shapely`_ is a Python package for manipulating and analysing two-dimensional geometric shapes.
Since version 2.0 it has included the function ``from_ragged_array`` which is ideally suited to
create Shapely geometries from contours created by ContourPy.

Contour lines to Shapely
------------------------

Contour lines with a line type of ``LineType.ChunkCombinedOffset`` are easily converted to Shapely
geometries using ``shapely.from_ragged_array``.

Here is the same example from the :ref:`line_type` section of the User Guide:

   >>> from contourpy import contour_generator
   >>> z = [[1.4, 1.2, 0.9, 0], [0.6, 3, 0.4, 0.7], [0.2, 0.2, 0.5, 3]]
   >>> cont_gen = contour_generator(z=z, line_type="ChunkCombinedOffset")
   >>> lines = cont_gen.lines(0.5)
   >>> lines
   ([array([[0.58, 1.], [1., 0.44], [1.38, 1.], [1., 1.36], [0.58, 1.], [2.6, 2.], [3., 1.57]])],
    [array([0, 5, 7], dtype=uint32)])

This has a single chunk containing one array of points and one array of offsets. To create
Shapely ``LineString`` geometries for this single chunk:

   >>> from shapely import GeometryType, from_ragged_array, unary_union
   >>> points, offsets = lines[0][0], lines[1][0]
   >>> linestrings = from_ragged_array(GeometryType.LINESTRING, points, (offsets,))
   >>> linestrings
   [<LINESTRING (2.444 0, 2 0.8, 1.962 1, 1 1.893, 0 1.25)>
    <LINESTRING (2 2, 2.333 1, 3 0.714)>]

where ``linestrings`` is a NumPy array of two Shapely LineStrings. To create a Shapely
MultiLineString instead you can either use ``shapely.unary_union`` on the LineStrings:

   >>> multilinestring = unary_union(linestrings)
   >>> multilinestring
   MULTILINESTRING ((2.444 0, 2 0.8, 1.962 1, 1 1.893, 0 1.25), (2 2, 2.333 1, 3 0.714))

or create them directly from the ContourPy ``lines`` using:

   >>> multilinestrings = from_ragged_array(GeometryType.MULTILINESTRING,
   ...                                      points, (offsets, [0, len(offsets)-1]))
   >>> multilinestrings
   [<MULTILINESTRING ((2.444 0, 2 0.8, 1.962 1, 1 1.893, 0 1.25), (2 2, 2.333 1,...>]

The ``shapely.unary_union`` approach returns a single MultiLineString whereas this approach returns
a NumPy array containing the single MultiLineString.

.. note::

   If your contour lines have a different line type then you can convert them using
   :func:`~.convert_lines`. If you have more than one chunk you can combine them using
   :func:`~.dechunk_lines` or iterate over the chunks, convert one chunk at a time and
   then combine the geometries.

Filled contours to Shapely
--------------------------

Filled contours with a fill type of ``FillType.ChunkCombinedOffsetOffset`` are easily converted to
Shapely geometries using ``shapely.from_ragged_array``.

Here is the same example from the :ref:`fill_type` section of the User Guide:

   >>> from contourpy import contour_generator
   >>> z = [[1.4, 1.2, 0.9, 0], [0.6, 3, 0.4, 0.7], [0.2, 0.2, 0.5, 3]]
   >>> cont_gen = contour_generator(z=z, fill_type="ChunkCombinedOffsetOffset")
   >>> filled = cont_gen.filled(1, 2)
   >>> filled
   ([array([[0., 0.], [1., 0.], [1.67, 0.], [1.77, 1.], [1., 1.71], [0.17, 1.], [0., 0.5],
            [0., 0.], [1., 0.44], [0.58, 1.], [1., 1.36], [1.38, 1.], [1., 0.44], [2.2 , 2.],
            [3., 1.13], [3., 1.57], [2.6, 2.], [2.2, 2.]])],
    [array([0, 8, 13, 18], dtype=uint32)],
    [array([0, 2, 3], dtype=uint32)])

This has a single chunk containing one array of points and two arrays of offsets which are the
boundary offsets and the polygon (outer boundary) offsets. To create Shapely ``Polygon`` geometries
for this single chunk:

   >>> from shapely import GeometryType, from_ragged_array, unary_union
   >>> points, offsets, outer_offsets = filled[0][0], filled[1][0], filled[2][0]
   >>> polygons = from_ragged_array(GeometryType.POLYGON, points, (offsets, outer_offsets))
   [<POLYGON ((0 0, 1 0, 1.667 0, 1.769 1, 1 1.714, 0.167 1, 0 0.5, 0 0), (1 0.4...>
    <POLYGON ((2.2 2, 3 1.13, 3 1.565, 2.6 2, 2.2 2))>]

where ``polygons`` is a NumPy array of two Shapely Polygons. To create a Shapely
MultiPolygon instead you can either use ``shapely.unary_union`` on the Polygons:

   >>> multipolygon = unary_union(polygons)
   >>> multipolygon
   <MULTIPOLYGON (((0 0, 1 0, 1.667 0, 1.769 1, 1 1.714, 0.167 1, 0 0.5, 0 0), ...>

or create them directly from the ContourPy ``filled`` using:

   >>> multipolygons = from_ragged_array(GeometryType.MULTIPOLYGON,
   ...                                   points,
   ...                                   (offsets, outer_offsets, [0, len(outer_offsets)-1]))
   >>> multipolygons
   [<MULTIPOLYGON (((0 0, 1 0, 1.667 0, 1.769 1, 1 1.714, 0.167 1, 0 0.5, 0 0), ...>]

The ``shapely.unary_union`` approach returns a single MultiPolygon whereas this approach returns
a NumPy array containing the single MultiPolygon.

.. note::

   If your filled contours have a different line type then you can convert them using
   :func:`~.convert_filled`. If you have more than one chunk you can combine them using
   :func:`~.dechunk_filled` or iterate over the chunks, convert one chunk at a time and
   then combine the geometries.

Example use of Shapely geometries
---------------------------------

As an example of what can be done with Shapely geometries, consider the single ``multipolygon``
created above. You can calculate the area

   >>> multipolygon.area
   2.143832

the bounding box

   >>> multipolygon.bounds
   bounds (0.0, 0.0, 3.0, 2.0)

and whether it contains particular points or not

   >>> from shapely import Point
   >>> multipolygon.contains(Point(2, 1))
   False
   >>> multipolygon.contains(Point(1.5, 1))
   True

.. note::

   You can use the ``polygons`` instead of the ``multipolygon`` here but first you will need to
   convert the array to a ``shapely.GeometryCollection`` first using:

   >>> from shapely import GeometryCollection
   >>> polygons = GeometryCollection(list(polygons))

.. _shapely_invalid:

Invalid geometry
----------------

As described in :ref:`limitations` it is possible for ContourPy to return contours with duplicate
points that are considered invalid by Shapely. To correct this use:

.. code-block:: python

   from shapely import is_valid, make_valid

   if not is_valid(polygon):
       polygon = make_valid(polygon)
