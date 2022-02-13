# standard library imports
from math import radians, tan, sqrt, atan, cos, sin
import time
from dataclasses import dataclass
import concurrent.futures
from rich import print

# third party imports
import plotly.graph_objects as go
from shapely.geometry import Polygon, LineString, Point, LinearRing, MultiPoint

# local imports
from data_validation import *


def mid_coord(p1, p2):
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


class Slope:
    def __init__(self, height=2, angle=30, length=None):

        # validate inputs
        assert_strictly_positive_number(height, "height")
        if angle is not None:
            # is allowed to be 90 but not 0
            assert_range(angle, "angle", 0, 90, not_low=True)
        if length is not None:
            assert_strictly_positive_number(length, "length")

        # if angle assigned instead of length work out the model length
        if not length:
            if not angle:
                raise ValueError(
                    "require angle of slope or length of slope to initialise"
                )
            length = height / tan(radians(angle))

        # determine model height and length as minimum of:
        # 4 * height and 5 * length AND minimum slope dimensions as below:
        MIN_EXT_H = 6
        MIN_EXT_L = 10
        tot_h = max(4 * height, MIN_EXT_H)
        tot_l = max(5 * length, MIN_EXT_L)

        # determine coordinates for edges of slope
        dx = (tot_l - length) / 2
        top = (dx, tot_h)
        bot = (dx + length, tot_h - height)

        # set up external boundary as a shapely LinearRing
        self._external_boundary = LinearRing(
            [(0, 0), (0, top[1]), top, bot, (tot_l, bot[1]), (tot_l, 0), (0, 0)]
        )

        # set relevant variables to self
        self.length = length
        self.height = height
        self._top_coord = top
        self._bot_coord = bot
        self._gradient = height / length

        # initialise empty properties used in other components of class
        self._materials = []
        self._water_depth = None
        self._search = {}
        self._min_FOS = 0
        self._slices = []

    def add_water_table(self, depth: int = 1):
        self._water_depth = depth

    def remove_water_table(self):
        self._water_depth = None

    def plot_boundary(self):
        # draw the external boundary
        x_, y_ = self._external_boundary.coords.xy
        fig = go.Figure(go.Scatter(x=list(x_), y=list(y_), mode="lines"))

        # following makes sure x and y are scaled the same, so that
        # model can be interpretted properly
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )

        # if there are no materials just return an empty shell
        if not self._materials:
            return fig

        # get the points representing the top line of the model
        # to help with drawing materials
        top = self._external_boundary.coords[1:3]

        # length of model (max x coordinate)
        tot_l = self._external_boundary.bounds[2]
        num_materials = len(self._materials)

        # loop through materials
        for i, m in enumerate(self._materials):
            # get reference level (y coordinate) for material
            y = m.RL

            # draw line for material boundary with extra meter to each side
            # to make sure there is a clear intersection (rather than points
            # just touching at boundary).
            long_line = LineString([(-1, y), (tot_l + 1, y)])

            # then get intersection to have definite material boundary
            line = self._external_boundary.intersection(long_line)

            # returns multipoint so convert simple tuple list
            line = [(p.x, p.y) for p in line.geoms]
            line.sort()

            # if the bot slope coordinate is between the bounds of the material
            # need to draw a bit differently
            if top[1][1] > self._bot_coord[1] and line[1][1] < self._bot_coord[1]:
                top.append(self._bot_coord)
                top.append((tot_l, self._bot_coord[1]))

            # if we are at the last material make the bottom the bottom of the model
            if i == num_materials - 1:
                bot = self._external_boundary.coords[-2:]
            else:
                bot = line

            # change bottom coordinates to be right to left
            # so points are arranged clockwise in a circle
            bot = sorted(bot, reverse=True)

            # get coordinates
            coords = top + bot
            x_ = [a[0] for a in coords]
            y_ = [a[1] for a in coords]

            fig.add_trace(
                go.Scatter(x=list(x_), y=list(y_), mode="lines", fill="toself")
            )

            # set the new top as the bottom, sort to put it back
            # to left to right order
            bot.sort()
            top = bot

        return fig

    def plot_critical(self):
        fig = self.plot_boundary()

        c_x, c_y, radius = self._min_FOS_location

        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=(c_x - radius),
            y0=(c_y - radius),
            x1=(c_x + radius),
            y1=(c_y + radius),
            line_color="LightSeaGreen",
        )

        fig.add_trace(
            go.Scatter(
                x=[c_x],
                y=[c_y],
                mode="lines+text",
                name="Lines and Text",
                text=[self._min_FOS],
                textposition="bottom center",
            )
        )

        return fig

    def add_materials(self, *materials):

        for material in materials:
            if not isinstance(material, Material):
                raise ValueError(
                    "The funciton add_materials only accepts instances of the Material Class"
                )

        l = [material.depth_to_bottom for material in materials]
        if len(l) > len(set(l)):
            raise ValueError("The same material depth has been input twice")

        # sort materials to be in order, include existing materials
        materials = list(materials) + self._materials
        materials.sort(key=lambda x: x.depth_to_bottom)

        # define RL for each material
        for material in materials:
            material.RL = self._top_coord[1] - material.depth_to_bottom

        self._materials = materials

    def remove_material(self, material=None, depth=None):
        # if material defined and material type and material in list then remove it
        if material and isinstance(material, Material):
            depth = material.depth_to_bottom
            return 1

        # if depth specified and had no luck removing material
        # try find the depth for a material in the list and then remove it
        if depth:
            for m in self._materials:
                if m.depth_to_bottom == depth:
                    self._materials.remove(m)
                    return 1

        return 0

    def analyse_circular_failure(self, c_x, c_y, radius):
        # get circle for analysis, note circle is actually a 64 sided polygon (not exact but close enough for calc)
        # https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
        p = Point(c_x, c_y)
        c = p.buffer(radius).boundary

        # find intersection points with boundary if any, else return None
        if c.intersects(self._external_boundary):
            i = c.intersection(self._external_boundary)
        else:
            return None

        # list for intersecting points between circle and external boundary
        i_list = []

        # loop through each point in the intersection list
        if not isinstance(i, MultiPoint):
            # something is wrong should be multipoint
            return None

        for p in i.geoms:
            # if point append x,y to list
            if isinstance(p, Point):
                i_list.append((round(p.x, 5), round(p.y, 5)))

            # might actually give a line string of the tiniest length
            # could happen due to 64 sided polygon if the circle is close to intersecting
            # at its end. In this case just use the first point of the line
            # since the points are close together anyways
            elif isinstance(p, LineString):
                i_list.append((round(p.coords[0][0], 5), round(p.coords[0][1], 5)))

        # make sure no input inside twice. Has been observed where the point of intersection
        # is the boundary between two linestrings
        i_list = list(set(i_list))
        i_list.sort()

        # check that there are only two intersecting points otherwise something is wrong
        if len(i_list) != 2:
            return None

        # total number of slices
        SLICES = 50

        # horizontal distance between left and right slice
        dist = i_list[1][0] - i_list[0][0]

        # width of a slice
        b = dist / SLICES

        # initialise left point of first slice
        s_x = i_list[0][0] + b / 2

        # intialise the push and resistance components for FOS before looping
        pushing = 0.0
        resisting = 0.0

        # loop through slice, actually want to iterate 1 time less than
        # the number of slices since we start at half a slice
        for slice in range(1, SLICES, 1):
            # define y coordinates for slice
            s_yb = c_y - sqrt(radius ** 2 - (s_x - c_x) ** 2)

            # get y coordinate at top
            # left of slope
            if s_x <= self._top_coord[0]:
                s_yt = self._top_coord[1]
            # right of slope
            elif s_x >= self._bot_coord[0]:
                s_yt = self._bot_coord[1]
            # on the slope
            else:
                # similiar triangles
                # minus because going to the right down
                # equation defining gradient just considers abs height on abs length
                s_yt = (-self._gradient) * (s_x - self._top_coord[0]) + self._top_coord[
                    1
                ]

            # get alpha, dy always positive, dx negative to right (uphill), dx positive to left
            # note alpha in radians by default
            dy = c_y - s_yb
            dx = c_x - s_x
            alpha = atan(dx / dy)

            # get height of unit
            h = s_yt - s_yb

            # get length
            l = b / cos(alpha)

            # intialize properties
            W = 0.0  # kN
            top = s_yt

            # loop through materials noting that they are already sorted by depth
            for m in self._materials:
                # while layers are higher than the top of the slice ignore the material
                if m.RL > s_yt:
                    continue
                # while the bottom of layer is in the slice consider, go from the
                # current top to the bottom of the layer
                # this captures the case of the top of the strip being partially in a layer
                elif m.RL < s_yt and m.RL > s_yb:
                    W += b * m.unit_weight * (top - m.RL)
                    top = m.RL
                # in the case that the bottom of the strip is now outside the range
                # we still have material between the current top and the bottom of the strip
                # we capture it in this edge case and then break since everything below can be ignored
                # we also grab the material properties at the base
                else:
                    W += b * m.unit_weight * (top - s_yb)
                    top = m.RL
                    cohesion = m.cohesion
                    friction_angle = m.friction_angle
                    break

            # check case that ran out of layers (loop terminated earlier than expected)
            if top > s_yb:
                m = self._materials[-1]
                W += b * m.unit_weight * (top - s_yb)
                top = m.RL
                cohesion = m.cohesion
                friction_angle = m.friction_angle

            # if there is a load on the strip apply it.
            if self._load_magnitude:
                load_xl, load_xr = self._load_location
                strip_xl = s_x - (b / 2)
                strip_xr = s_x + (b / 2)
                # case 1 clearly no load
                if load_xr <= strip_xl or load_xl >= strip_xr:
                    pass
                # case 2 clearly load is completely inside
                elif load_xl <= strip_xl and load_xr >= strip_xr:
                    W += b * self._load_magnitude
                # case 3 on the left inside the load
                elif strip_xl <= load_xl and strip_xr >= load_xl:
                    W += (strip_xr - load_xl) * self._load_magnitude

                # case 4 on the right side of the load
                elif strip_xl <= load_xr and strip_xr >= load_xr:
                    W += (load_xr - strip_xl) * self._load_magnitude

                else:
                    raise ValueError("ummm is this actually a possible case?")

            if self._water_depth:
                U = max(min(self._water_depth, s_yt) - s_yb, 0) * 9.81
            else:
                U = 0

            resisting += cohesion * l + (W * cos(alpha) - U) * tan(
                radians(friction_angle)
            )
            pushing += W * sin(alpha)
            if pushing == 0:
                stop = True

            # initialise slice x coordinate for next loop
            s_x = s_x + b

        return resisting / pushing

    def analyse_slope(self):
        # Approx number of runs
        ITERATIONS = 2000

        # 10 * 10 * 5 = 500
        # allow for 3 mid points of slope
        # 3 * 10 * 5 = 150 (minimum) - 650 min iterations

        NUMBER_CIRCLES = 5

        # generate coordinates for left of slope
        point_combinations = ITERATIONS / NUMBER_CIRCLES
        NUMBER_POINTS = int((3 + sqrt(9 + 4 * point_combinations)) / 2)

        x1, x2, x3, x4 = (
            0,
            self._top_coord[0],
            self._bot_coord[0],
            self._external_boundary.bounds[2],
        )
        y1, y3 = self._top_coord[1], self._bot_coord[1]

        # split top and bottom slope up into 10 coordinate points
        left_coords = [
            ((n / NUMBER_POINTS) * (x2 - x1), y1) for n in range(1, NUMBER_POINTS + 1)
        ]
        right_coords = [
            (x3 + (n / NUMBER_POINTS) * (x4 - x3), y3) for n in range(NUMBER_POINTS)
        ]

        # add in 3 coordinates for the slope
        p1, p5 = self._top_coord, self._bot_coord
        p3 = mid_coord(p1, p5)
        p2 = mid_coord(p1, p3)
        p4 = mid_coord(p3, p5)
        left_coords += [p2, p3, p4]

        search = {}
        threads = []

        # loop through left and right coordinates and generate a circular slope
        # that passes through these points
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for l_c in left_coords:
                for r_c in right_coords:
                    search.update(
                        self.run_analysis_for_circles(l_c, r_c, NUMBER_CIRCLES)
                    )
        #             f1 = executor.submit(self.run_analysis_for_circles, l_c,r_c,NUMBER_CIRCLES)
        #             threads.append(f1)
        #             # multi thread circle calc thing

        # for f in concurrent.futures.as_completed(threads):
        #     search.update(f.result())

        self._search = search
        self._min_FOS_location = min(search, key=search.get)
        self._min_FOS = search[self._min_FOS_location]

    def run_analysis_for_circles(self, l_c, r_c, NUMBER_CIRCLES=5):
        # assume a starting circle that has a straight vertical slope down at the top of the slope
        # this means the centre of the circle is in line with the top of the slope
        # since the tangent of the circle is perpendicular to the centre

        # angle of slope of choord (For circular slope)
        beta = atan((l_c[1] - r_c[1]) / (r_c[0] - l_c[0]))

        # half of the circle coord that passess from top of point to bottom of point
        half_coord_distance = sqrt((l_c[1] - r_c[1]) ** 2 + (r_c[0] - l_c[0]) ** 2) / 2

        # starting circle details
        start_radius = half_coord_distance / cos(beta)
        start_centre = (l_c[0] + start_radius, l_c[1])
        start_chord_to_centre = sqrt(start_radius ** 2 - half_coord_distance ** 2)
        start_chord_to_edge = start_radius - start_chord_to_centre

        # two intersecting chords through circle have segments of chords related
        # as a * b = c * d , where a and b are the lengths of chord on each side of intersection
        # as such we have half_coord_distance ** 2 = chord_to_edge * (R + (R-chord_to_edge)) = C
        C = half_coord_distance ** 2

        # loop through circles
        search = {}

        for i in range(0, NUMBER_CIRCLES):

            # doesnt include going all the way in which we dont want to do anyways
            chord_to_edge = start_chord_to_edge * (NUMBER_CIRCLES - i) / NUMBER_CIRCLES
            radius = circle_radius_from_abcd(chord_to_edge, C)
            centre = circle_centre(
                beta=beta,
                chord_intersection=mid_coord(l_c, r_c),
                chord_to_centre=radius - chord_to_edge,
            )
            c_x, c_y = centre

            FOS = self.analyse_circular_failure(c_x, c_y, radius)
            if FOS:
                # search[(c_x,c_y,radius)] = FOS
                search[(l_c[0], r_c[0], radius)] = FOS
            else:
                break

        return search

    def add_surcharge(self, offset=0, load=20, length=None):

        right_x = self._top_coord[0] - offset
        if length:
            left_x = max(0, right_x - length)
        else:
            left_x = 0

        # note that this is slightly different than most coordinates
        # in that it isnt a LineString and doesnt have y coordinate
        # also, could add functionality for different loads to apply
        # in future
        self._load_magnitude = load
        self._load_location = [left_x, right_x]

    def remove_surcharge(self):
        self._load_magnitude = 0


@dataclass
class Material:
    unit_weight: float = 20
    friction_angle: int = 35
    cohesion: int = 2
    depth_to_bottom: int = 5

    def __repr__(self):
        return f"Material(uw={self.unit_weight},phi={self.friction_angle},c={self.cohesion},d_bot={self.depth_to_bottom}"


if __name__ == "__main__":
    s = Slope(height=3, angle=30, length=None)

    fill = Material(20, 30, 5, 1)
    granular = Material(20, 35, 0, 5)

    s.add_materials(fill, granular)

    s.add_surcharge(0.5, 20)

    t1 = time.perf_counter()
    s.analyse_slope()
    print(
        f"Took {time.perf_counter()-t1} seconds to process {len(s._search.keys())} runs"
    )
    print(s._min_FOS)
    print(s._min_FOS_location)
