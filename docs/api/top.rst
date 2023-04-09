contourpy
---------

.. automodule:: contourpy

.. autoclass:: FillType

.. autoclass:: LineType

.. autoclass:: ZInterp


.. autofunction:: contour_generator

.. autofunction:: max_threads


.. autoclass:: ContourGenerator
   :members:
   :exclude-members: create_contour, create_filled_contour

   .. property:: default_fill_type
      :classmethod:

      Return the default ``FillType`` used by this algorithm.

   .. property:: default_line_type
      :classmethod:

      Return the default ``LineType`` used by this algorithm.

.. autoclass:: Mpl2005ContourGenerator
   :show-inheritance:

.. autoclass:: Mpl2014ContourGenerator
   :show-inheritance:

.. autoclass:: SerialContourGenerator
   :show-inheritance:

.. autoclass:: ThreadedContourGenerator
   :show-inheritance:
