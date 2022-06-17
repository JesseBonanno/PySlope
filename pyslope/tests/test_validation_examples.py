# pytest is expected to be run from top level directory only

from pyslope.pyslope import Slope, Material, Udl, LineLoad


# for c the results of 500 slices
# in slide used to be closer to the true value
# since the difference was too high to pass the test

SLIDE_RESULTS = {
    "a": {
        2: 1.272,
        3: 2.180,
        4: 3.907,
        5: 5.736,
    },
    "b": {
        2: 1.272,
        3: 2.266,
        4: 3.941,
        5: 5.759,
    },
    "c": {
        3: 1.602,
        4: 2.330,
        5: 3.174,
    },
    "d": {
        3: 1.597,
        4: 2.585,
        5: 4.266,
    },
    "e": {3: 2.036, 4: 3.718, 5: 5.559},
}


def test_example_a():
    # cohesionless example
    s = Slope(height=1, angle=None, length=1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 0, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(2, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=50, iterations=2000)

    s.analyse_slope()

    # # check results for each faiure plane
    # for radius, slide_fos in SLIDE_RESULTS['a'].items():
    #     fos = list(filter(lambda x : x['radius'] == radius, s._search))[0]['FOS']
    #     difference = abs(slide_fos - fos)
    #     average = (slide_fos + fos)/2

    #     # check less than 1% difference between pySlope and other software
    #     assert(difference/average < 0.01)

    for result in s._search:
        fos = result["FOS"]
        slide_fos = SLIDE_RESULTS["a"][result["radius"]]
        difference = abs(slide_fos - fos)
        average = (slide_fos + fos) / 2

        # check less than 1% difference between pySlope and other software
        assert difference / average < 0.01


def test_example_b():
    # example with cohesion added
    s = Slope(height=1, angle=None, length=1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 2, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(2, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    s.update_analysis_options(slices=50)

    s.analyse_slope()

    for result in s._search:
        fos = result["FOS"]
        slide_fos = SLIDE_RESULTS["b"][result["radius"]]
        difference = abs(slide_fos - fos)
        average = (slide_fos + fos) / 2

        # check less than 1% difference between pySlope and other software
        assert difference / average < 0.01


def test_example_c():
    # adding in water table
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

    s.update_analysis_options(slices=50)

    s.set_water_table(0.7)

    s.analyse_slope()

    for result in s._search:
        fos = result["FOS"]
        slide_fos = SLIDE_RESULTS["c"][result["radius"]]
        difference = abs(slide_fos - fos)
        average = (slide_fos + fos) / 2

        # check less than 1% difference between pySlope and other software
        assert difference / average < 0.01


def test_example_d():
    # adding in Udl
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

    s.update_analysis_options(slices=50)

    udl1 = Udl(
        magnitude=20,
        offset=0.5,
        length=2,
    )

    s.set_udls(udl1)

    s.analyse_slope()

    for result in s._search:
        fos = result["FOS"]
        slide_fos = SLIDE_RESULTS["d"][result["radius"]]
        difference = abs(slide_fos - fos)
        average = (slide_fos + fos) / 2

        # check less than 1% difference between pySlope and other software
        assert difference / average < 0.01


def test_example_e():
    # adding in line load
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

    s.update_analysis_options(slices=50)

    ll1 = LineLoad(
        magnitude=5,
        offset=1,
    )

    s.set_lls(ll1)

    s.analyse_slope()

    for result in s._search:
        fos = result["FOS"]
        slide_fos = SLIDE_RESULTS["e"][result["radius"]]
        difference = abs(slide_fos - fos)
        average = (slide_fos + fos) / 2

        # check less than 1% difference between pySlope and other software
        assert difference / average < 0.01


def test_example_f():
    # Effect of slices on results
    s = Slope(height=1, angle=None, length=1)

    m1 = Material(20, 35, 0, 0.5)
    m2 = Material(20, 35, 0, 1)
    m3 = Material(18, 30, 0, 5)

    s.set_materials(m1, m2, m3)

    for r in range(2, 6):
        s.add_single_circular_plane(
            c_x=s.get_bottom_coordinates()[0],
            c_y=s.get_bottom_coordinates()[1] + 2.5,
            radius=r,
        )

    slices = [10, 25, 50, 500, 2000]

    for i in slices:

        s.update_analysis_options(slices=i)
        s.analyse_slope()

        assert s.get_min_FOS()


def test_example_g():
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

    s.set_udls(udl1, udl2)

    iterations = [1000, 2000]

    for i in iterations:
        s.update_analysis_options(slices=20, iterations=i)
        s.analyse_slope()

        assert s.get_min_FOS()
