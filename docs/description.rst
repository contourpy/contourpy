.. _algorithm_description:

Algorithm description
=====================

Overview
--------

The locations of contour lines are determined by interpolation of the gridded ``z`` values.
Consider contouring at a z-level of ``level``. Firstly, each unmasked ``z`` value is classified as
being above the ``level`` or not. In Python notation this would be ``is_above = z > level``.

.. note::

   In words we label grid points as being either **above** or **below** the contour level, but note
   that points that are exactly on the contour level are labelled as below. They have to be in one
   of the two classifications and below is the historic convention.

The edge of each quad is then considered, and if one of its end points is above the contour level
and the other below, then the contour crosses that edge. The (x, y) position where the contour
level crosses the edge is determined by interpolation (see :ref:`z_interp`).

A single quad can have 0, 2 or 4 contour points, up to one per edge, depending upon how the contour
line intersects it. The contour points are connected together in a predictable order with higher
``z`` on the left as you follow them around.

If ``quad_as_tri=False`` then the points are connected with straight lines across each quad.  The
only complexity here are quads that intersect the contour line on all four edges. Here the two
contour lines that enter the quad can either turn left or right to leave the quad, and it is not
immediately obvious which is preferable. These quads are called saddle quads.  The solution is to
calculate the effective ``z`` of the central virtual point, and if it is above the contour level
then the contour lines turn to the right, otherwise they turn to the left, thus keeping higher ``z``
on the left as usual.

If ``quad_as_tri=True`` then each full (i.e. not corner masked) quad is divided into four triangles
using a central virtual point, and extra points are inserted into each contour line that cross such
a quad depending on where the ``level`` intersects the diagonals from the central point.

All that is left to do is join together the contour line segments from each quad into a set of
closed line loops and open line strips. Usually the algorithms are designed to make this as
efficient as possible by some combination of sweeping through the domain a row or column at a time
and following contour lines around the domain.

Filled contours are more complicated in that they may consist of lines on the lower and/or upper
contour levels as well as parts of the domain boundary, including masked out regions. The order of
points on the lower contour level is the same as for contour lines with higher ``z`` on the left,
but the order of points on the upper contour level is the opposite with higher ``z`` is on the
right.

Detailed
--------

This section describes in more detail the algorithm used by the ``serial`` and ``threaded``
contour generators.

Each contour generator stores a cache of flags for each quad that is used for fast lookup. Some of
the flags refer to the grid and are constant for the lifetime of the contour generator, some of them
change during each call to :func:`~contourpy.SerialContourGenerator.lines` and
:func:`~contourpy.SerialContourGenerator.filled`.

When created, a contour generator initialises the cache with information about the grid including
which quads are masked out or corner-masked, and which edges are boundaries of either the domain,
masked regions, or the edges of chunks.

At the start of each call to :func:`~contourpy.SerialContourGenerator.lines` or
:func:`~contourpy.SerialContourGenerator.filled`, the non-grid cache flags are set. These are the
z-levels, i.e. whether the ``z`` values are above or below the contour levels, and also flags that
indicate possible starting points for contour lines or filled contours.  Each contour line and
filled contour will have at least one starting flag set in the cache, many will have more than one.

The main algorithm processes each chunk independently, and has two passes of what is usually known
as a marching squares, sweep or scan algorithm. This progresses through the grid a quad at a time.
If a quad is reached that is flagged as a starting point, the march is halted and the contour line
is followed through the domain. When the end of the line is reached the march is resumed.

The first pass does the following:

#. Counts the total number of points and lines followed.
#. Erases start flags that are no longer needed.
#. If it is calculating filled contours and the ``fill_type`` requires the relationship between
   outer boundary and their holes, flags are set in the cache for this.
#. Sets extra cache flags for rows in the domain that do not contain any start flags to speed up
   the second pass.

At the end of the first pass a buffer is allocated to contain all of the contour points, and one or
more offset buffers depending upon the ``line_type`` or ``fill_type``.

The second pass does the following:

#. Calculates and stores the contour points.
#. Stores the offsets of the starts and ends of each contour line.
#. Stores the relationship between the outer boundaries and their holes, if required.

The sequence of operations is slightly different in the second pass if the relationship between
outer boundaries and their holes is required. The outer boundary is always followed first, and as
this occurs the starting quads of its holes are determined from the cache and when the outer is
finished, its holes are immediately followed too. This ensures that each outer and its holes are
contiguous in the points and offsets arrays.
