# to benchmark speed
from pyslope import Slope, Material, Udl, LineLoad

s = Slope(height=1, angle=None, length=1.5)

m1 = Material(20, 40, 1, 0.3)
m2 = Material(20, 35, 2, 1)
m3 = Material(18, 30, 0, 1.5)
m4 = Material(16, 27, 0.1, 2)
m5 = Material(17, 22, 0, 3)
m6 = Material(19, 28, 0, 5)


s.set_materials(m1, m2, m3, m4, m5, m6)

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

s.update_analysis_options(slices=100, iterations=2500)

s.set_analysis_limits(
    left_x=1,
    right_x=8,
    left_x_right=3,
    right_x_left=6,
)

s.set_udls(udl1, udl2)

s.analyse_slope()
