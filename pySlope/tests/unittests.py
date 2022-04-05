from multiprocessing.sharedctypes import Value
import os
import sys
sys.path.insert(0, os.path.abspath('../'))

import unittest
import pytest
from pySlope import Material, Slope
from utilities import mid_coord, circle_radius_from_abcd, circle_centre, dist_points, reset_results

class MaterialTestCase(unittest.TestCase):
    def test_init(self):
        sand = Material(
            unit_weight=10,
            friction_angle=30,
            cohesion = 2,
            depth_to_bottom = 1,
            name = 'sand',
            color = 'red'
        )
        clay = Material()

    def test_bad_values(self):
        with pytest.raises(ValueError):
            Material(unit_weight='')

        with pytest.raises(ValueError):
            Material(unit_weight=0)

        with pytest.raises(ValueError):
            Material(unit_weight=-10)

        with pytest.raises(ValueError):
            Material(friction_angle='')

        with pytest.raises(ValueError):
            Material(friction_angle=-50)

        with pytest.raises(ValueError):
            Material(cohesion='')

        with pytest.raises(ValueError):
            Material(cohesion=-50)

        with pytest.raises(ValueError):
            Material(depth_to_bottom='')

        with pytest.raises(ValueError):
            Material(depth_to_bottom='')

        with pytest.raises(ValueError):
            Material(cohesion=-50)
        
        with pytest.raises(ValueError):
            Material(depth_to_bottom='')

        with pytest.raises(ValueError):
            Material(depth_to_bottom=-50)

        with pytest.raises(AssertionError):
            Material(name=1)
        
        with pytest.raises(AssertionError):
            Material(color=1)

class SlopeTestCase(unittest.TestCase):

    def test_init(self):

        # things that should work
        a = Slope()
        b = Slope(
            height = 2,
            angle = 20,
        )
        c = Slope(
            height = 5,
            length = 5,
        )

        #things that shouldn't work
        with pytest.raises(ValueError):
            Slope(
                height = None
            )

        with pytest.raises(ValueError):
            Slope(
                angle = None,
                length = None
            )

        with pytest.raises(ValueError):
            Slope(
                height = -5
            )

        with pytest.raises(ValueError):
            Slope(
                angle = -5
            )

        with pytest.raises(ValueError):
            Slope(
                angle = 92
            )

if __name__ == '__main__':
    unittest.main(verbosity=2)