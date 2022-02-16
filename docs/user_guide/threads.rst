.. _threads:

Threads
-------

The ``threaded`` algorithm supports the use of multiple threads.

.. name_supports::
   :filter: threads

.. warning::

   The threaded algorithm is work in progress and should be considered experimental.  It works fine
   in an isolated environment using the ``contourpy`` tests and benchmarks, but needs to be
   rigorously tested in real-world environments that that include mixed Python/C++ code and multiple
   threads before it can be considered production quality.

``threaded`` shares most of its code with ``serial`` except for the high-level processing of chunks
which it performs in parallel using a thread pool, and the creation of `NumPy`_ arrays is limited to
a single thread at a time.

.. note::

   The domain must be divided into chunks for multithreaded contouring.

Create a :class:`~contourpy.ThreadedContourGenerator` by calling
:func:`~contourpy.contour_generator` in the usual way, ensuring that the domain is chunked:

   >>> from contourpy import contour_generator
   >>> import numpy as np
   >>> z = np.ones((100, 50))  # Sample z data.
   >>> cont_gen = contour_generator(z=z, name="threaded", chunk_count=5, thread_count=4)
   >>> cont_gen.thread_count
   4
   >>> cont_gen.chunk_count
   25

Here the 25 chunks will be divided up between the 4 threads.

The ``thread_count`` argument is optional, if not specified the default is ``thread_count=0`` which
means it will use the maximum number of threads available. This number can be checked using:

   >>> import contourpy
   >>> contourpy.max_threads()

.. note::

   :func:`contourpy.max_threads()` is implemented using the C++ function
   `std::thread::hardware_concurrency
   <https://en.cppreference.com/w/cpp/thread/thread/hardware_concurrency>`_.

If you request more threads than the number of chunks, the thread count will be reduced accordingly.

.. warning::

   The order of processing chunks is not deterministic. If you use a :class:`~contourpy.LineType` or
   :class:`~contourpy.FillType` that do not arrange the results by chunk, the order of
   returned lines/polygons is also not deterministic. This includes ``LineType.Separate``,
   ``LineType.SeparateCode``, ``FillType.OuterCode`` and ``FillType.OuterOffset``.
