Calculation with chunks
-----------------------

This page shows the performance of the ``serial`` algorithm as the ``total_chunk_count`` is
increased from 1 to 120.

.. image:: ../_static/chunk_lines_simple_light.svg
   :class: only-light

.. image:: ../_static/chunk_lines_simple_dark.svg
   :class: only-dark

.. image:: ../_static/chunk_filled_simple_light.svg
   :class: only-light

.. image:: ../_static/chunk_filled_simple_dark.svg
   :class: only-dark

The performance of the  ``simple`` dataset varies by only a small amount (4%) for a
``total_chunk_count`` of up to 120.

.. image:: ../_static/chunk_lines_random_light.svg
   :class: only-light

.. image:: ../_static/chunk_lines_random_dark.svg
   :class: only-dark

.. image:: ../_static/chunk_filled_random_light.svg
   :class: only-light

.. image:: ../_static/chunk_filled_random_dark.svg
   :class: only-dark

For the ``random`` dataset the variations are greater at up to 14% and are usually, but not always,
slower for increasing ``total_chunk_count``.
