contourpy.util
--------------

.. automodule:: contourpy.util

This module includes ``Renderer`` classes for both `Bokeh`_ and  `Matplotlib`_ to visualise contours
calculated by ContourPy. These renderers are used internally in the test suite and for examples in
this documentation. Please use them to experiment with ContourPy, but it is recommended that you
don't use them in downstream projects as they are liable to change at short notice without a
formal deprecation period. Instead use `Bokeh`_ and  `Matplotlib`_  directly as they both use
ContourPy for their contour calculations and they provide much richer visualisation functionality.

.. automodule:: contourpy.util.renderer
   :members:

.. automodule:: contourpy.util.bokeh_renderer
   :members:

.. automodule:: contourpy.util.mpl_renderer
   :members: MplRenderer
