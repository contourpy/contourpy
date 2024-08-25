.. _limitations:

Limitations
-----------

Duplicate contour points
^^^^^^^^^^^^^^^^^^^^^^^^

It is possible for calculated contour lines and filled polygons to contain identical adjacent
points. This can occur when contouring a z-level that exactly matches the value at a grid point.

As an example, consider calculating contour lines at ``z=0.1`` on a grid of a single quad with one
corner at ``z=0`` and the other three at ``z=1``:

  >>> from contourpy import contour_generator
  >>> cont_gen = contour_generator(z=[[0, 1], [1, 1]])
  >>> cont_gen.lines(0.1)
  [array([[0. , 0.1],
          [0.1, 0. ]])]

The returned contour line has two points, from ``(0, 0.1)`` to ``(0.1, 0)``.

If you contour a z-value of ``z=0.01``:

  >>> cont_gen.lines(0.1)
  [array([[0.  , 0.01],
          [0.01, 0.  ]])]

the contoured points are correspondingly closer to the ``z=0`` corner.

If the contoured z-level is ``0``, exactly matching the z-value of the corner:

  >>> cont_gen.lines(0)
  [array([[0., 0.],
          [0., 0.]])]

then the returned contour line still has two points but they are identical, exactly the same as the
corner's ``(x, y)`` location.

Similar applies to filled contours so that it is possible for a filled contour polygon to have
multiple duplicate points and zero area.

Depending on what you are doing with the calculated contours, this may or may not be a problem.
If you are using them with `Shapely`_ for example, they might be considered invalid; see
:ref:`shapely_invalid` for how to deal with this.
