.. _docstrings:

===========================
pySlope Reference
===========================
Material
---------
.. autoclass:: pyslope.Material

Uniform Distributed Load (Udl)
---------------------------------
.. autoclass:: pyslope.Udl

Line Load
------------
.. autoclass:: pyslope.LineLoad

Slope
----------
.. autoclass:: pyslope.Slope

Slope: Geometry
~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pyslope.Slope.set_external_boundary
.. autofunction:: pyslope.Slope.get_top_coordinates
.. autofunction:: pyslope.Slope.get_bottom_coordinates
.. autofunction:: pyslope.Slope.get_external_y_intersection
.. autofunction:: pyslope.Slope.get_external_x_intersection


Slope: Initialising Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pyslope.Slope.set_water_table
.. autofunction:: pyslope.Slope.remove_water_table
.. autofunction:: pyslope.Slope.set_udls
.. autofunction:: pyslope.Slope.remove_udls
.. autofunction:: pyslope.Slope.set_lls
.. autofunction:: pyslope.Slope.remove_lls
.. autofunction:: pyslope.Slope.set_materials
.. autofunction:: pyslope.Slope.remove_material
.. autofunction:: pyslope.Slope.set_analysis_limits
.. autofunction:: pyslope.Slope.remove_analysis_limits

Slope: Options
~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pyslope.Slope.update_water_analysis_options
.. autofunction:: pyslope.Slope.update_analysis_options
.. autofunction:: pyslope.Slope.update_boundary_options


Slope: Failure Planes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pyslope.Slope.add_single_circular_plane
.. autofunction:: pyslope.Slope.remove_individual_planes
.. autofunction:: pyslope.Slope.add_single_entry_exit_plane


Slope: Analysing
~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pyslope.Slope.analyse_slope
.. autofunction:: pyslope.Slope.analyse_dynamic


Slope: Results
~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pyslope.Slope.get_min_FOS
.. autofunction:: pyslope.Slope.get_min_FOS_circle
.. autofunction:: pyslope.Slope.get_min_FOS_end_points
.. autofunction:: pyslope.Slope.get_dynamic_results

Slope: Plotting
~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: pyslope.Slope.plot_boundary
.. autofunction:: pyslope.Slope.plot_critical
.. autofunction:: pyslope.Slope.plot_all_planes