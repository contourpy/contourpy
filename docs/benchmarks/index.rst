.. _benchmarks:

Benchmarks
==========

``contourpy`` uses ``asv`` (`airspeed velocity <https://asv.readthedocs.io>`_) for benchmarking.

To run the entire benchmarking suite:

.. code-block:: bash

   $ pip install asv virtualenv
   $ cd benchmarks
   $ asv run

This will benchmark the latest commit of the ``main`` branch. When this is finished you can display
the results in a web browser using:

.. code-block:: bash

   $ asv publish
   $ asv preview

For further information see the ``README.md`` document in the ``benchmarks`` directory.

There follows a summary of key benchmark results taken on a 6-core Intel Core i7-10750H processor
for commit ``f3e864e``.

.. toctree::
   :maxdepth: 1

   calculation
   rendering
   threads

.. note::

   If you want to reproduce these plots for your own hardware, run the benchmarks locally as
   described above and then run the ``plot_benchmarks.py`` script to extract the benchmark results
   and generate the plots.  Some tweaking of plot parameters may be required to get them looking
   nice.
