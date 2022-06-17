# pytest is expected to be run from top level directory only

from pyslope.pyslope import Slope, Material, Udl, LineLoad
import pytest


@pytest.fixture(scope="module")
def s():
    s = Slope(height=1, angle=None, length=1.5)

    m1 = Material(20, 40, 1, 0.3)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 1.5)
    m4 = Material(16, 28, 0, 5)

    s.set_materials(m1, m2, m3, m4)

    ll1 = LineLoad(
        magnitude=5,
        offset=0.5,
    )

    ll2 = LineLoad(
        magnitude=20,
        offset=2.5,
    )

    s.set_lls(ll1, ll2)

    udl1 = Udl(
        magnitude=100,
        offset=1,
        length=0.5,
    )

    udl2 = Udl(
        magnitude=300,
        length=0.5,
        offset=3,
    )

    s.update_water_analysis_options(auto=False, H=0.98)

    s.update_analysis_options(
        slices=10, iterations=500, min_failure_dist=1, max_iterations=10, tolerance=0.01
    )

    s.set_analysis_limits(
        left_x=1,
        right_x=8,
        left_x_right=3,
        right_x_left=6,
    )

    s.set_udls(udl1, udl2)

    s.analyse_slope()

    yield s


def test_plot_boundary(s):
    s.plot_boundary()


def test_plot_critical(s):
    s.plot_critical()


def test_plot_all_planes(s):
    s.plot_all_planes(2)
