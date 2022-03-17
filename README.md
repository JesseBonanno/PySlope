# PySlope

[![CodeFactor](https://www.codefactor.io/repository/github/jessebonanno/pyslope/badge?s=43db3d31fb1ca55747ede7e5205c7d9e0cf37ced)](https://www.codefactor.io/repository/github/jessebonanno/pyslope)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JesseBonanno/pySlope/main?filepath=demo.ipynb)

Slope stability module based on bishops method of slices

## Example

```python
# import required classes
from pySlope import Slope, Material, Udl, PointLoad

# initialise slope object with height and angle (or height and length)
s = Slope(height=3, angle=30, length=None)

# Create two geotechnical material layers
m1 = Material(unit_weight=20,friction_angle=35,cohesion=3,depth_to_bottom=1, name='Fill')
m2 = Material(20,30,0,5, name = 'Sand')

# Create two uniformly distributed loads
u1 = Udl(magnitude = 100, offset=2, length=5)
u2 = Udl(magnitude = 20)

# Create line load / Point Load
p1 = PointLoad(magnitude = 10, offset = 3)

# Assign geotechnical layers, and loads to slope
s.set_materials(m1,m2)
s.set_udls(u1, u2)
s.set_pls(p1)

# Assign Water table 4 m below top of slope
s.set_water_table(4)

# Update analysis option so that piezometric head is automatically calculated on slope
s.update_water_analysis_options(auto=True)

# analyse the slope
s.analyse_slope()

# print the minimum FOS
print(s.get_min_FOS())

# get a graph showing the critical failure
fig = s.plot_critical()

# get a graph showing all failure planes with a factor of safety less than 2
fig = s.plot_all_planes(max_fos=2)
```

The script above produces the following figures:
![plot_critical](https://github.com/JesseBonanno/pySlope/blob/main/examples/critical.png)
![plot_all_planes](https://github.com/JesseBonanno/pySlope/blob/main/examples/all_planes.png)
