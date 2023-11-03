.. _chunks:

Chunks
------

The domain to contour can be divided up into a number of chunks that are processed separately.

Advantages of using chunks:

- They produce shorter lines/polygons that may be simpler or faster to render.
- They make subsequent spatial queries easier.
- They allow the use of multithreaded contouring (see :ref:`threads`).

Disadvantages:

- There is a slight performance cost of using chunks.
- Some rendering algorithms show faint lines between neighbouring chunks.

.. note::

   Think of chunks as dividing the quads rather than the points of a domain. A ``z`` array of shape
   ``(ny, nx)`` has ``(ny, nx)`` points but only ``(ny-1, nx-1)`` quads.  This can be considered a
   single chunk of shape ``(ny-1, nx-1)``.  Neighbouring chunks have neighbouring quads but they
   share the points that lie on their common boundary.

There are three possible ways of specifying chunks in :func:`~contourpy.contour_generator` which
are the keyword arguments ``chunk_size``, ``chunk_count`` and ``total_chunk_count``. A maximum of
one of the three may be specified.

.. warning::

   You may not always receive the chunk sizes or counts that you request. A chunk has a minimum
   size of 1x1 quad!

chunk_size
^^^^^^^^^^

``chunk_size`` may be a tuple of ``(y_chunk_size, x_chunk_size)`` or a single integer that is used
for both x and y chunk sizes.

   >>> z = np.ones((5, 10))  # Sample z data.
   >>> cont_gen = contour_generator(z=z, chunk_size=(2, 4))
   >>> cont_gen.chunk_size
   (2, 4)
   >>> cont_gen.chunk_count
   (2, 3)

The final chunk in each direction may be smaller than the others. Here in the x-direction there are
3 chunks of size 4; the first two x-chunks cover 8 quads leaving the final x-chunk to cover just a
single quad.

chunk_count
^^^^^^^^^^^

``chunk_count`` may be a tuple of ``(y_chunk_count, x_chunk_count)`` or a single integer that is
used for both x and y chunk counts.

Using ``chunk_count`` can give more even chunks than using ``chunk_size``.

total_chunk_count
^^^^^^^^^^^^^^^^^

``total_chunk_count`` attempts to give a sensible combination of x and y chunk counts.

It uses a simple algorithm that finds two integer factors that are close as possible to
``sqrt(total_chunk_count)``. Do not use a prime number for ``total_chunk_count`` as the two factors
it will use are ``total_chunk_count`` and ``1``.
