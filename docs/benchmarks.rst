Benchmarks
==========

``contourpy`` uses ``asv`` (`airspeed velocity <https://asv.readthedocs.io>`_) for benchmarking.

To run the entire benchmarking suite:

.. code-block:: bash

   $ pip install asv virtualenv pyperf
   $ cd benchmarks
   $ asv run

This will benchmark the latest commit of the ``main`` branch. When this is finished you can display
the results in a web browser using:

.. code-block:: bash

   $ asv publish
   $ asv preview

For further information on using ``asv`` see
`https://asv.readthedocs.io <https://asv.readthedocs.io>`_.

To follow: summary of important results from benchmarking and explanation of difference.