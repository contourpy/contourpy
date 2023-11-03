
z array, mask and corner mask
-----------------------------

.. _z_array:

z array
^^^^^^^

The ``z`` array is the 2D array of values to calculate the contours of and is the only compulsory
argument to :func:`~contourpy.contour_generator`. It can be specified in any form that is
convertible to a 2D `NumPy`_ array of ``dtype=np.float64``, such as nested Python lists.

Within the C++ code it is stored as a contiguous C-ordered ``np.float64`` array. If it is not
already in this format it will be converted to it and hence the underlying data will be copied.
You can avoid this copy by passing it in the desired format.

.. warning::

   If the ``z`` array does not need to be copied then both the :class:`~contourpy.ContourGenerator`
   and your client code have access to the same shared array. This means that you can purposefully
   or accidentally alter the data that the :class:`~contourpy.ContourGenerator` is using, which is
   almost certainly not a good idea! Here is an example of this:

   >>> from contourpy import contour_generator
   >>> import numpy as np
   >>> from sys import getrefcount
   >>> z = np.asarray([[0., 0.], [1., 1.]])
   >>> getrefcount(z)
   2
   >>> cont_gen = contour_generator(z=z)
   >>> getrefcount(z)
   3

   ``z`` is a contiguous C-ordered ``np.float64`` array and the change in reference counts shows
   that the :class:`~contourpy.ContourGenerator` is using this ``z`` array.

    >>> cont_gen.lines(0.5)
    [array([[0. , 0.5],
            [1. , 0.5]])]

   Now change an element of the ``z`` array that is used by the :class:`~contourpy.ContourGenerator`
   and repeat the same :func:`~contourpy.ContourGenerator.lines` call:

   >>> z[0, 0] = -1.
   >>> cont_gen.lines(0.5)
   [array([[0.  , 0.75],
           [1.  , 0.5 ]])]

   The output is different.

.. _z_mask:

Mask
^^^^

The ``z`` array passed to :func:`~contourpy.contour_generator` can be a
`NumPy masked array <https://numpy.org/doc/stable/reference/maskedarray.html>`_ to mask out specific
grid points from contour calculations.  In addition, any ``z`` values which are non-finite
(``np.inf`` or ``np.nan``) will also be masked out.

.. note::

   The mask of a ``z`` array is used only when constructing a :class:`~contourpy.ContourGenerator`
   object, so there is no danger that a mask shared with client code can subsequently be altered to
   change the behaviour of the :class:`~contourpy.ContourGenerator`.

Corner mask
^^^^^^^^^^^

The boolean ``corner_mask`` keyword argument passed to :func:`~contourpy.contour_generator` is used
to control how much of the domain is masked out by masked ``z`` values.

If ``corner_mask=False`` all quads that touch a masked out point are completely masked out.
If ``corner_mask=True`` then only the triangular corners of quads nearest masked out points are
always masked out, other corners that contain three unmasked points are contoured as usual.

Here is an example of the difference, the red circles indicate masked out points:

.. plot::
   :separate-modes:
   :source-position: below

   import numpy as np
   from contourpy import contour_generator
   from contourpy.util.mpl_renderer import MplRenderer as Renderer

   x, y = np.meshgrid(np.arange(7), np.arange(6))
   z = np.sin(x*np.pi/6)*np.sin(y*np.pi/5)
   mask = np.zeros_like(z, dtype=bool)
   mask[(0, 2, 2, 4, 5), (0, 2, 3, 4, 1)] = True
   z = np.ma.array(z, mask=mask)

   levels = np.linspace(0.0, 1.0, 4)
   renderer = Renderer(ncols=2, figsize=(6, 3))

   for ax, corner_mask in enumerate([False, True]):
       cont_gen = contour_generator(x, y, z, corner_mask=corner_mask)

       for i in range(len(levels)-1):
           filled = cont_gen.filled(levels[i], levels[i+1])
           renderer.filled(filled, cont_gen.fill_type, ax=ax, color=f"C{i}")

       renderer.grid(x, y, ax=ax, color="gray", alpha=0.2)
       renderer.mask(x, y, z, ax=ax, color="red")
       renderer.title(f"corner_mask = {corner_mask}", ax=ax)

   renderer.show()

All algorithms other than ``mpl2005`` support corner masking, and it is enabled by default on those
algorithms that support it if you do not specifically request otherwise via ``corner_mask=False``.

.. name_supports::
   :filter: corner_mask
