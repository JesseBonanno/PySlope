.. _docstrings:

===========================
pySlope Reference
===========================
Material
---------
.. autoclass:: pySlope.Material

Uniform Distributed Load (Udl)
---------------------------------
.. autoclass:: pySlope.Udl

Line Load
------------
.. autoclass:: pySlope.PointLoad

Slope
-------
.. autoclass:: pySlope.Slope
.. autofunction:: pySlope.Slope.set_external_boundary
.. autofunction:: pySlope.Slope.set_water_table
.. autofunction:: pySlope.Slope.remove_water_table
.. autofunction:: pySlope.Slope.set_udls
.. autofunction:: pySlope.Slope.remove_udls
.. autofunction:: pySlope.Slope.set_pls
.. autofunction:: pySlope.Slope.remove_pls
.. autofunction:: pySlope.Slope.set_materials
.. autofunction:: pySlope.Slope.remove_material
.. autofunction:: pySlope.Slope.update_water_analysis_options
.. autofunction:: pySlope.Slope.update_analysis_options
.. autofunction:: pySlope.Slope.update_boundary_options
.. autofunction:: pySlope.Slope.set_analysis_limits
.. autofunction:: pySlope.Slope.remove_analysis_limits
.. autofunction:: pySlope.Slope.analyse_circular_failure
.. autofunction:: pySlope.Slope.analyse_slope
.. autofunction:: pySlope.Slope.analyse_dynamic
.. autofunction:: pySlope.Slope.get_min_FOS
.. autofunction:: pySlope.Slope.get_min_FOS_circle
.. autofunction:: pySlope.Slope.get_min_FOS_end_points
.. autofunction:: pySlope.Slope.get_dynamic_results
.. autofunction:: pySlope.Slope.plot_boundary
.. autofunction:: pySlope.Slope.plot_critical
.. autofunction:: pySlope.Slope.plot_all_planes