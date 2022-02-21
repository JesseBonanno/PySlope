# standard library imports
from math import cos, sin, sqrt
from shapely.geometry import Point
from colour import Color

def mid_coord(p1 : Point, p2 : Point) -> Point:
    return [(a + b) / 2 for a, b in zip(p1, p2)]

def dist_points(p1:tuple, p2:tuple) -> float:
    return sqrt(abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1]) ** 2 )


def circle_radius_from_abcd(c_to_e, C):
    # two intersecting chords through circle have segments of chords related
    # as a * b = c * d , where a and b are the lengths of chord on each side of intersection
    # as such we have half_coord_distance ** 2 = chord_to_edge * (R + (R-chord_to_edge)) = C

    return (C + c_to_e ** 2) / (2 * c_to_e)


def circle_centre(beta, chord_intersection, chord_to_centre):
    dy = cos(beta) * chord_to_centre
    dx = sin(beta) * chord_to_centre

    return [a + b for a, b in zip(chord_intersection, (dx, dy))]


def create_fos_color_dictionary():
    colors = [
        (0,'red'),
        (1,'orange'),
        (2,'green'),
        (3,'blue'),
    ]

    colors.sort(key = lambda x : x[0])

    color_dict = {}

    for i in range(len(colors)-1):
        c1 = Color(colors[i][1])
        c2 = Color(colors[i+1][1])

        p1 = colors[i][0]
        p2 = colors[i+1][0]

        d = int((p2 - p1)*10)

        color_range = list(c1.range_to(c2,d+1))

        for f in range(d+1):
            color_dict[round(f/10+p1,1)] = color_range[f].hex

    return color_dict

COLOUR_FOS_DICT = create_fos_color_dictionary()





    

    
