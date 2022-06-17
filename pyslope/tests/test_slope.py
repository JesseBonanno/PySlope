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

    s.set_water_table(1)

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


def test_material_remove():
    # check for a random slope
    s = Slope(height=1, angle=45)
    m1 = Material(unit_weight=40, friction_angle=30, depth_to_bottom=2)
    s.set_materials(
        m1,
        Material(depth_to_bottom=6),
    )

    for r in range(2, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=10, iterations=100)
    s.analyse_slope()

    fos = s.get_min_FOS()

    # update and remove the same material by depth
    s.set_materials(
        Material(unit_weight=25, cohesion=1000, depth_to_bottom=5),
    )

    s.remove_material(depth=5)

    s.analyse_slope()
    assert fos == s.get_min_FOS()

    # update and remove a material by instance
    s.remove_material(m1)
    s.set_materials(m1)
    s.analyse_slope()
    assert fos == s.get_min_FOS()

    # remove all and check materials empty
    s.remove_material(remove_all=True)
    assert s._materials == []


def test_remove_water_table():
    # adding in water table
    s = Slope(height=1, angle=45, length=1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(3, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=10)

    s.set_water_table(0.7)

    s.analyse_slope()

    fos = s.get_min_FOS()

    s.remove_water_table()

    s.analyse_slope()

    assert fos <= s.get_min_FOS()


def test_remove_limits():
    s = Slope(height=1, angle=None, length=1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(3, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=10)

    s.set_analysis_limits(0, 8)
    s.remove_analysis_limits()


def test_remove_udl():
    s = Slope(height=1, angle=None, length=1)
    u1 = Udl(20)
    s.set_udls(u1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(3, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=10)

    s.analyse_slope()

    fos = s.get_min_FOS()

    s.remove_udls(u1)
    s.set_udls(u1)
    s.analyse_slope()
    fos2 = s.get_min_FOS()

    s.remove_udls(remove_all=True)
    s.set_udls(u1)
    s.analyse_slope()
    fos3 = s.get_min_FOS()

    assert fos == fos2 == fos3


def test_remove_ll():
    s = Slope(height=1, angle=None, length=1)
    ll1 = LineLoad(20)
    s.set_lls(ll1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(3, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=10)

    s.analyse_slope()

    fos = s.get_min_FOS()

    s.remove_lls(ll1)
    s.set_lls(ll1)
    s.analyse_slope()
    fos2 = s.get_min_FOS()

    s.remove_lls(remove_all=True)
    s.set_lls(ll1)
    s.analyse_slope()
    fos3 = s.get_min_FOS()

    assert fos == fos2 == fos3


def test_remove_individual_planes():
    s = Slope(height=1, angle=None, length=1)
    ll1 = LineLoad(20)
    s.set_lls(ll1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(3, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=10, iterations=1000)

    s.analyse_slope()

    assert len(s._search) == 3

    s.remove_individual_planes()
    s.analyse_slope()

    assert len(s._search) > 800
    assert len(s._search) < 1200


def test_dynamic_analysis():
    s = Slope(height=1, angle=None, length=1)
    ll1 = LineLoad(magnitude=20, dynamic_offset=True)
    s.set_lls(ll1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    s.update_analysis_options(slices=10, iterations=500)

    s.analyse_dynamic()

    s.print_dynamic_results()
    assert s.get_dynamic_results()


def test_custom_color():
    s = Slope(height=1, angle=None, length=1)
    ll1 = LineLoad(magnitude=20, dynamic_offset=True, color="purple")
    s.set_lls(ll1)

    m1 = Material(20, 35, 0, 0.5, color="ienagind")
    m2 = Material(20, 35, 2, 1, color="green")
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(3, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.analyse_slope()

    s.plot_critical()
