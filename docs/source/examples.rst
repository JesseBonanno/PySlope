.. _examples:

1. Introduction to Examples
==============================

This section demonstrates the core functionality of the ``pySlope`` package with examples.

You can follow along with examples online: |binder|

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/JesseBonanno/pySlope/main?filepath=pySlope%2Fexamples%2Freadme_example.ipynb


2. Basic Usage (Readme example)
============================================================

2.1 Overview
+++++++++++++++++++

Let's walk through a typical use case to investigate the slope shown in the figure below.

.. figure:: examples/readme_example_plot_boundary.png
  :width: 700
  :alt: slope_boundary_plot

A typical use case of the `pySlope` package involves the following steps:

1. Create a `Slope` object
2. Create `Material` objects and assign to `Slope`
3. Create `Udl` or `PointLoad` objects and assign to `Slope`
4. Set water table
5. Set analysis limits
6. Analyse slope for critical factor of safety
7. Create plots


2.2 Creating a Slope
------------------------

Concept
++++++++++

The creation of a `Slope` instance involves the input of the:

   - slope height (m) and
   - angle (deg) or
   - length (m)

Only one of the values is used out of the length and angle, the other value should be set to None.



Code
+++++++++++++++++++

``s = Slope(height=3, angle=30, length=None)``

::

s = Slope(height=3, angle=30, length=None)

