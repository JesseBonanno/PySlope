# PySlope

[![License](https://img.shields.io/badge/license-MIT-lightgreen.svg)](https://github.com/JesseBonanno/pySlope/blob/main/LICENSE.txt)
[![CodeFactor](https://www.codefactor.io/repository/github/jessebonanno/pyslope/badge?s=43db3d31fb1ca55747ede7e5205c7d9e0cf37ced)](https://www.codefactor.io/repository/github/jessebonanno/pyslope)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JesseBonanno/pySlope/main?filepath=pySlope%2Fexamples%2Freadme_example.ipynb)
[![DOI](https://jose.theoj.org/papers/10.21105/jose.00111/status.svg)](https://doi.org/10.21105/jose.00111)
[![Documentation Status](https://readthedocs.org/projects/pySlope/badge/?version=main)](https://pyslope.readthedocs.io/en/latest)

pySlope is a 2D slope stability module based on bishops method of slices. This module allows for the following parameters:
   - unlimited horizontal geological units
   - water table
   - uniform loads
   - line loads
   - slope search limits
 
This module can return plots for the critical failure slope or plots for all failure slopes below a certain factor of safety.

The module can perform 2500 iterations with 50 slices in approximately 3 seconds.

## Project Purpose

The purpose of this project is two fold:

   1. Create a free online slope stability software
   2. Provide a pythonic solution to implementing Bishop's method based on object oriented coding principles

Performing a slope stability calculation by hand is extremely uneconimical and time consuming. 

The problem involves a lot of geometrical mathematics which can make the calculation hard to achieve with only excel. Python packages exist for geometrical mathematics which makes it well suited to implementing a slope stability analysis package. There is however, no well-documented open-source slope stability software that can currently be found online. This package aims to fill that gap.

## Functionality and usage

A typical use case of the `pySlope` package involves the following steps:

1. Create a `Slope` object
2. Create `Material` objects and assign to `Slope`
3. Create `Udl` or `PointLoad` objects and assign to `Slope`
4. Set water table
5. Set analysis limits
6. Analyse slope for critical factor of safety
7. Create plots

You can follow along with this example below in this web-based binder jupyter notebook. [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JesseBonanno/pySlope/main?filepath=pySlope%2Fexamples%2Freadme_example.ipynb)

### Creating a Slope

The creation of a `Slope` instance involves the input of the:

   - slope height (m) and
   - angle (deg) or
   - length (m)

Only one of the values is used out of the length and angle, the other value should be set to None.

```python
s = Slope(height=3, angle=30, length=None)
```

### Defining Materials

The creation of a `Material` object involves the input of:

   - unit weight (kN/m3)
   - friction angle
   - cohesion (kPa)
   - depth from top of slope to bottom of material layer (m)

Once a material is defined it can then be assigned to the `Slope` instance.

```python
m1 = Material(
    unit_weight=20,
    friction_angle=45,
    cohesion=2,
    depth_to_bottom=2
)
m2 = Material(20, 30, 2, 5)    # Material defined with positional arguments
s.set_materials(m1, m2)        # An unlimited number of materials can be assigned at one time
```

The slope will know to order the materials based on the depth to the bottom of the strata so the order that the materials are provided isn't important. It is important that the same depth isnt provided twice for two different materials, and attempting this will raise an error.

### Defining Uniform Loads

The creation of a `Udl` (uniform distributed load) object involves the input of:

   - magnitude of load (kPa)
   - offset of load from crest of slope (m) (default 0 m)
   - length of load (m) (default infinite)

```python
u1 = Udl(magnitude = 100, offset = 2, length = 1)

# by default offset = 0 (m) and length = None.
u2 = Udl(magnitude = 20)    

# assign uniform loads to model 
s.set_udls(u1, u2)
```

### Defining Line Loads

The creation of a `PointLoad` object involves the input of:
   - magnitude of load (kN / m)
   - offset of load from crest of slope (m) (default 0 m)

```python

# define line load, similiar to Udl except there is no length parameter and magnitude is in units (kN/m)
p1 = PointLoad(magnitude = 10, offset = 3)

# assign point loads to slope
s.set_pls(p1)
```

### Defining Water Table

By default there is no water table. The water table is defined by its depth from the top of the slope (m).

```python
s.set_water_table(4)
```

### Defining Analysis Limits

Analysis limits can be specified as a general left and right limit, OR as a set of limits which control the range from which the top of failures can occur and the bottom of failures can occur.

Currently the model coordinates are dynamic in that the overall model dimensions are based on the size of the slope.

A simple workaround method is to use the following values `s._top_slope[0]` which represents the x coordinate of the crest of the slope, and `s._bot_slope[0]` which represents the x coordinate of the toe of the slope.

```python
s.set_analysis_limits(s._top_coord[0]-5,s._bot_coord[0]+5)
```

### Analysing Slope

To analyse the `Slope` the analyse_slope() method is called. By default 2500 iterations are run with 50 slices per failure plane.

```python
# The user can change the number of slices and iterations with the method below.
# The line below is implicitly called and only required by the user if they want to change iterations
s.update_analysis_options(slices=50, iterations=2500)

# run analysis
s.analyse_slope()

### Interpretting results

After analysing the slope the critical factor of safety can be taken as below.

```python
print(s.get_min_FOS())
```

A more useful output might be a plot. Currently there are 3 main plots that can be called.

```python
s.plot_boundary()  # plots only the boundary
s.plot_critical()  # plots the boundary with the critical failure of the slope
s.plot_all_planes(max_fos=i) # plots boundary with all slope failures below fos i (where i is number)

Examples of the plots are shown below. 

![example_1 plot critical](https://github.com/JesseBonanno/pySlope/blob/main/pySlope/examples/readme_example_plot_critical.png)
![example_1 plot all slopes fos less than 2](https://github.com/JesseBonanno/pySlope/blob/main/pySlope/examples/readme_example_plot_all_maxfos2.png)

### Dynamic Analysis

Instead of standard static analysis the user also has the option to make load objects *dynamic*. The user can then perform a dynamic analysis rather than static, which moves the load in order to determine the required offset for a minimum factor of safety.

Considering the example above, we can continue and make u1 dynamic.

```python
# remove udl object load from slope
s.remove_udls(u1)

# now lets add the udl again but this time set the load as 'dynamic'
# for all loads and materials we also have the option to set the color ourselves
# lets try set the color as 'purple'
s.set_udls(
    Udl(magnitude=100, length=1, offset=2, dynamic_offset=True, color='purple')
)

# run dynamic analysis aiming for a FOS of 1.2
s.analyse_dynamic(critical_fos=1.2)

# get dictionary of all determined minimum FOS with key value pairing of offset : value
print(s.get_dynamic_results())

# can be better printed out as
for k,v in s.get_dynamic_results().items():
    print('Offset:', round(k,3), ' m, FOS:', round(v,3))
```

From this we get the following output results:

Offset: 0  m, FOS: 1.016
Offset: 5.186  m, FOS: 1.471
Offset: 2.098  m, FOS: 1.26
Offset: 1.584  m, FOS: 1.232
Offset: 1.352  m, FOS: 1.204
Offset: 1.324  m, FOS: 1.198
Offset: 1.332  m, FOS: 1.2

We can also get a plot as after running dynamic analysis all plots are based on the final iteration of the dynamic analysis.

![example_1 plot all slopes fos less than 2](https://github.com/JesseBonanno/pySlope/blob/main/pySlope/examples/readme_example_plot_dynamic.png)


## Installing the package

Currently this repository is not being distributed as a python package. To use, feel free to fork the code.

## Future Work

There is a lot of room for expansion of the project, and the direction of the project will strongly be affected by open-source contribution from the community. Some things in the short to medium term scope of work are:

- host online web based application to use
- Shift graphing from backend to front end for web application
- better documentation
- unit testing
- other analysis methods
- faster plotting

## Contributing

The guidelines for contributing are specified [here](https://github.com/JesseBonanno/pySlope/blob/main/CONTRIBUTING.md).

## Support

The guidelines for support are specified [here](https://github.com/JesseBonanno/pySlope/blob/main/SUPPORT.md).


## License

[![License](https://img.shields.io/badge/license-MIT-lightgreen.svg)](https://github.com/JesseBonanno/pySlope/blob/main/LICENSE.txt)
