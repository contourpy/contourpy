.. _quickstart:

Quick start
===========

Contour generator
-----------------

Firstly create a simple 2x2 grid of ``z`` values using Python lists:

  >>> z = [[0.0, 0.1], [0.2, 0.3]]

Import the :func:`~contourpy.contour_generator` function and call it to create and return the
:class:`~contourpy.ContourGenerator` object that will be used to contour the ``z`` values:

  >>> from contourpy import contour_generator
  >>> cont_gen = contour_generator(z=z)
  >>> cont_gen
  <contourpy._contourpy.SerialContourGenerator object at 0x7ff827fc4a30>

The hexadecimal number will be different, it is the address of the `pybind11`_-wrapped C++ object.

Contour lines
-------------

Create some contour lines at a z-level of ``0.25``:

  >>> lines = cont_gen.lines(0.25)
  >>> lines
  [array([[0.5, 1.0],
          [1. , 0.75]])]

The output is a list of lines, here just one line that is a `NumPy`_ array of shape ``(2, 2)``
consisting of two ``(x, y)`` points from ``(0.5, 1)`` to ``(1, 0.75)``.

.. note::

   The format of data returned by :meth:`~contourpy.ContourGenerator.lines` is controlled by
   the ``line_type`` argument passed to :func:`~contourpy.contour_generator`.

Filled contours
---------------

Create some filled contours between the z-levels of ``0.15`` and ``0.25``:

  >>> filled = cont_gen.filled(0.15, 0.25)
  >>> filled
  ([array([[0. , 1.  ],
           [0. , 0.75],
           [1. , 0.25],
           [1. , 0.75],
           [0.5, 1.  ],
           [0. , 1.  ]])],
   [array([0, 6], dtype=uint32)])

The output data is more complicated, it is a tuple of two lists each of which has a length of one
corresponding to a single polygon. The first `NumPy`_ array has shape ``(6, 2)`` and is the
``(x, y)`` coordinates of the 6 points that make up the polygon; the first and last points are the
same. The second `NumPy`_ array is an integer array of offsets into the points array; here the
offsets cover the whole length of the points array indicating that it is a single polygon. This is
explained further in :ref:`fill_type`.

.. note::

   The format of data returned by :meth:`~contourpy.ContourGenerator.filled` is controlled by
   the ``filled_type`` argument passed to :func:`~contourpy.contour_generator`.

Graphical output
----------------

It is easier to understand the contour lines and filled contours by looking at graphical output.
Here is the full example using the `Matplotlib`_ renderer from the :mod:`contourpy.util` module:

.. plot::
   :separate-modes:
   :source-position: below

   from contourpy import contour_generator
   from contourpy.util.mpl_renderer import MplRenderer as Renderer

   z = [[0.0, 0.1], [0.2, 0.3]]
   cont_gen = contour_generator(z=z)
   lines = cont_gen.lines(0.25)
   filled = cont_gen.filled(0.15, 0.25)

   renderer = Renderer(figsize=(4, 2.5))
   renderer.filled(filled, cont_gen.fill_type, color="gold")
   renderer.lines(lines, cont_gen.line_type, color="red", linewidth=2)
   renderer.show()

Alternatively you can use the `Bokeh`_ renderer from the :mod:`contourpy.util.bokeh_renderer`
module. In the example above change the line

.. code-block:: python

   from contourpy.util.mpl_renderer import MplRenderer as Renderer

into

.. code-block:: python

   from contourpy.util.bokeh_renderer import BokehRenderer as Renderer

Output for the `Bokeh`_ renderer is sent to your web browser.
