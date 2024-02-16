Algorithm name
--------------

There are four possible algorithms to use for contouring which are identified by the ``name``
keyword argument passed to :func:`~.contour_generator`. For example:

  >>> cont_gen = contour_generator(name="serial", ...)

The four names are :ref:`mpl2005`, :ref:`mpl2014`, :ref:`serial` and :ref:`threaded`.
The default is :ref:`serial`, which you should use unless you have a good reason not to.

There are four optional features that the algorithms may support, which are ``corner_mask``,
``quad_as_tri``, ``threads`` and ``z_interp``. This table indicates which algorithms supports which
feature:

.. name_supports::

Also, some algorithms only support a subset of the possible :class:`~.LineType`
and :class:`~.FillType` enums; these are discussed in :ref:`line_type` and :ref:`fill_type`
respectively.

.. _mpl2005:

mpl2005
^^^^^^^

The original 2005 Matplotlib algorithm, modified to conform to the ContourPy API and so that it
can be wrapped using `pybind11`_. Does not support any of ``corner_mask``, ``quad_as_tri``,
``threads`` or ``z_interp``.

.. warning::

   This algorithm is in ``contourpy`` for historic comparison. No new features or bug fixes will be
   added to it, except for security-related bug fixes.

.. _mpl2014:

mpl2014
^^^^^^^

The 2014 Matplotlib algorithm, a replacement of the original 2005 algorithm that added
``corner_mask`` and made the code easier to understand.  Modified to conform to the ContourPy
API and so that it can be wrapped using `pybind11`_.  Does not support ``quad_as_tri``, ``threads``
or ``z_interp``.

.. warning::

   This algorithm is in ``contourpy`` for historic comparison. No new features or bug fixes will be
   added to it, except for security-related bug fixes.

.. _serial:

serial
^^^^^^

The default algorithm for ContourPy, released in 2022, which supports all of the optional
features except for ``threads``. It combines lessons learnt from both of the previous algorithms as
well as adding new features and performance improvements.

.. _threaded:

threaded
^^^^^^^^

This is a multithreaded version of the :ref:`serial` algorithm, and requires the domain to be divided
into chunks.  It shares the majority of its code with :ref:`serial` except:

#. High-level processing of chunks occurs in parallel using a thread pool.
#. Creation of `NumPy`_ arrays is limited to a single thread at a time.
