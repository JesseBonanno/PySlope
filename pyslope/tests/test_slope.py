# pytest is expected to be run from top level directory only

from pyslope.pyslope import Slope


def test_is_slope():
    s = Slope()
    assert isinstance(s, Slope)
