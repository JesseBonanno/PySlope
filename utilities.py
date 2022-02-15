# standard library imports
from math import cos, sin
from shapely.geometry import Point


def mid_coord(p1 : Point, p2 : Point) -> Point:
    return [(a + b) / 2 for a, b in zip(p1, p2)]


def circle_radius_from_abcd(c_to_e, C):
    # two intersecting chords through circle have segments of chords related
    # as a * b = c * d , where a and b are the lengths of chord on each side of intersection
    # as such we have half_coord_distance ** 2 = chord_to_edge * (R + (R-chord_to_edge)) = C

    return (C + c_to_e ** 2) / (2 * c_to_e)


def circle_centre(beta, chord_intersection, chord_to_centre):
    dy = cos(beta) * chord_to_centre
    dx = sin(beta) * chord_to_centre

    return [a + b for a, b in zip(chord_intersection, (dx, dy))]