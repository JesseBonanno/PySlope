# standard library imports
from math import radians, tan, sqrt, atan, cos, sin
import time
from dataclasses import dataclass
# import concurrent.futures
from colour import Color

# third party imports
import plotly.graph_objects as go
from shapely.geometry import Polygon, LineString, Point, LinearRing, MultiPoint
from tqdm import tqdm
from rich import print

# local imports
from data_validation import *
from utilities import mid_coord, circle_radius_from_abcd, circle_centre, dist_points
from utilities import COLOUR_FOS_DICT

@dataclass
class Material:
    unit_weight: float = 20
    friction_angle: int = 35
    cohesion: int = 2
    depth_to_bottom: int = 5

    def __repr__(self):
        return f"Material(uw={self.unit_weight},phi={self.friction_angle},c={self.cohesion},d_bot={self.depth_to_bottom}"

class Slope:
    
    def __init__(self, height : float = 2, angle : int = 30, length : float = None):
        """Initialise a slope object"""

        # intialise options
        self.update_options(slices=50, iterations=2500, MIN_EXT_H=6, MIN_EXT_L=10)
        
        self.set_external_boundary(height=height,angle=angle,length=length)

        # initialise empty properties used in other components of class
        self._materials = []
        self._water_RL = None
        self._load_magnitude = 0



    def set_external_boundary(self,height : float = 2, angle : int = 30, length : float = None):
        """Set external boundary for model.

        Parameters
        ----------
        height : int, optional
            height of slope in metres, by default 2
        angle : int, optional
            angle of slope in degrees (may be left as none if slope
            is instead expressed by length of slope), by default 30
        length : int, optional
            length of slope in metres (may be left as none if slope
            is instead expressed by angle of slope), by default None

        Raises
        ------
        ValueError
            If input not in required range or of required type
        """

        # validate inputs
        assert_strictly_positive_number(height, "height")
        if angle is not None:
            # is allowed to be 90 but not 0
            assert_range(angle, "angle", 0, 90, not_low=True)
        if length is not None:
            assert_positive_number(length, "length")

        # if angle assigned instead of length work out the model length
        if length is None:
            if not angle:
                raise ValueError(
                    "require angle of slope or length of slope to initialise"
                )
            length = height / tan(radians(angle))

        MIN_EXT_H = self._MIN_EXT_H
        MIN_EXT_L = self._MIN_EXT_L

        tot_h = max(4 * height, MIN_EXT_H, 5 * length/2)
        tot_l = max(5 * length, MIN_EXT_L, 4 * height)

        # determine coordinates for edges of slope
        dx = (tot_l - length) / 2
        top = (dx, tot_h)
        bot = (dx + length, tot_h - height)

        # set up external boundary as a shapely LinearRing
        self._external_boundary = LinearRing(
            [(0, 0), (0, top[1]), top, bot, (tot_l, bot[1]), (tot_l, 0), (0, 0)]
        )

        # set relevant variables to self
        self._length = length
        self._height = height

        if angle == 90 or length == 0:
            self._gradient = 100000000000000
        else:
            self._gradient = height / length

        self._top_coord = top
        self._bot_coord = bot

        self._external_length = self._external_boundary.bounds[2]
        self._external_height = self._external_boundary.bounds[3]

        # reset results to deal with case that boundary is changed after
        # an analysis has already taken place.
        self._reset_results()

    def set_water_table(self, depth: int = 1):
        """set water table value """
        assert_positive_number(depth, "water depth")
        self._water_RL = max(0, self._top_coord[1] - depth)

    def remove_water_table(self):
        """Remove water table from model"""
        self._water_RL = None

    def set_surcharge(self, offset : float = 0, load : float = 20, length : float = None):
        """set a surface surcharge on top of the slope

        Parameters
        ----------
        offset : int, optional
            offset from the crest of the slope in metres, by default 0
        load : int, optional
            load magnitude in kPa, by default 20
        length : _type_, optional
            length of the load across the model (perpendicular to slope
            ) in metres. If length is None or length exceeds edge of model, 
            then length set to left edge of model, by default None
        """
        assert_positive_number(offset, "offset")
        assert_positive_number(load, "load")
        assert_positive_number(length, "length")

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
        """ Remove surcharge from model. """
        self._load_magnitude = 0

    def set_materials(self, *materials):
        """Assign material instances to the slope instance.

        Parameters
        ----------
        *materials : Material (list), optional
            Material instances to be associated with slope.


        Raises
        ------
        ValueError
            If material not instance of Material class error is raised.
        ValueError
            If non-unique material depths then error is raised.
        """

        for material in materials:
            if not isinstance(material, Material):
                raise ValueError(
                    "The function add_materials only accepts instances of the Material Class"
                )

        # sort materials to be in order, include existing materials
        materials = list(materials) + self._materials
        materials.sort(key=lambda x: x.depth_to_bottom)

        depths = [material.depth_to_bottom for material in materials]

        if len(depths) > len(set(depths)):
            raise ValueError("The same material depth has been input twice")

        # define RL for each material
        for material in materials:
            material.RL = self._top_coord[1] - material.depth_to_bottom

        self._materials = materials

    def remove_material(self, material : Material = None, depth : float = None):
        """Remove material from slope.

        Parameters
        ----------
        material : Material, optional
            material object. If specified and exists in materials
            associated with slope then will be removed, by default None
        depth : float, optional
            depth in metres of material object. If not None and material found
            at indicated depth then will remove the material, by default None

        """
        # if material defined and material type and material in list then remove it
        if material and isinstance(material, Material):
            depth = material.depth_to_bottom

        # if depth specified and had no luck removing material
        # try find the depth for a material in the list and then remove it
        if depth:
            assert_positive_number(depth, "material depth")
            for m in self._materials:
                if m.depth_to_bottom == depth:
                    self._materials.remove(m)

    def update_options(self, slices : int = None, iterations : int = None, MIN_EXT_L : float = None, MIN_EXT_H : float = None):
        """Function to update general modelling options.

        Parameters
        ----------
        slices : int, optional
            Slices to take in calculation for each potential 
            circular failureIf None doesnt update the parameter, by default None
        iterations : int, optional
            Approximate number of potential slopes to check.
            If None doesnt update the parameter, by default None
        MIN_EXT_L : float, optional
            Minimum external boundary length. If None doesnt update
            the parameter, by default None
        MIN_EXT_H : float, optional
            Minimum external boundary height. If None doesnt update
            the parameter, by default None.
        """

        if slices:
            assert_range(slices,'slices',10,500)
            self._slices = slices
        if iterations:
            assert_range(iterations,'iterations',1000,100000)
            self._iterations = iterations
        if MIN_EXT_H:
            assert_strictly_positive_number(MIN_EXT_H,'Minimum external model height (MIN_EXT_H)')
            self._MIN_EXT_H = MIN_EXT_H
            self.set_external_boundary(height=self._height,length=self._length)
        if MIN_EXT_L:
            assert_strictly_positive_number(MIN_EXT_L,'Minimum external model length (MIN_EXT_H)')
            self._MIN_EXT_L = MIN_EXT_L
            self.set_external_boundary(height=self._height,length=self._length)
        
    def analyse_circular_failure(self, c_x : float, c_y : float, radius : float):
        """Calculate factor of safety for a circular failure plane through the slope.

        Parameters
        ----------
        c_x : float
            circle center x coordinate
        c_y : float
            circle center y coordinate
        radius : float
            circle radius

        Returns
        -------
        float
            factor of safety
        None
            if cant calculate returns None
            
        """
        # data validation
        assert_strictly_positive_number(c_x,'c_x (circle x coordinate)')
        assert_strictly_positive_number(c_y,'c_y (circle y coordinate)')
        assert_strictly_positive_number(radius,'radius')


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
        if len(i_list) > 1:
            i_list= i_list[0:2]
        else:
            return None

        # total number of slices
        SLICES = self._slices

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

            if self._water_RL:
                U = max(min(self._water_RL, s_yt) - s_yb, 0) * 9.81 * l
            else:
                U = 0

            resisting += cohesion * l + max(0,(W * cos(alpha) - U)) * tan(
                radians(friction_angle)
            )
            pushing += W * sin(alpha)
            if pushing == 0:
                stop = True

            # initialise slice x coordinate for next loop
            s_x = s_x + b

        if pushing <= 0:
            return None

        return (resisting / pushing, i_list[0], i_list[1])

    def analyse_slope(self, deep_seeded_only=False):
        """Analyse many possible failure planes for a slope.

        Parameters
        ----------
        deep_seeded_only : bool, optional
            If true doesnt define failures through the slope,
            only around the slope, by default False.

        Returns
        ----------
        Nothing but sets the following in the instance:
        
        self._MIN_FOS
        self._search
        self._MIN_FOS_LOCATION

        """
        # Approx number of runs
        ITERATIONS = self._iterations

        GRADIENT_TOLERANCE = 10

        # # seems like 15 % of runs dont happen every time for some reason,
        # # possibly just general geometry clashes
        # ITERATIONS = ITERATIONS 

        # 10 * 10 * 5 = 500
        # allow for 3 mid points of slope
        # 3 * 10 * 5 = 150 (minimum) - 650 min iterations

        NUMBER_CIRCLES = max(5,int(ITERATIONS/1000))

        NUMBER_POINTS_SLOPE = max(5,int(ITERATIONS/800))

        # generate coordinates for left of slope
        point_combinations = ITERATIONS / NUMBER_CIRCLES
        
        if deep_seeded_only:
            NUMBER_POINTS = int(sqrt(point_combinations))
        else:
            if self._gradient > GRADIENT_TOLERANCE:
                NUMBER_POINTS = int((NUMBER_POINTS_SLOPE+sqrt(NUMBER_POINTS_SLOPE**2+4*point_combinations))/2) - NUMBER_POINTS_SLOPE
            else:
                NUMBER_POINTS = int(sqrt(point_combinations)) - NUMBER_POINTS_SLOPE

        x1, x2, x3, x4 = (
            0,
            self._top_coord[0],
            self._bot_coord[0],
            self._external_length,
        )
        y2, y3 = self._top_coord[1], self._bot_coord[1]

        # split top and bottom slope up into 10 coordinate points
        left_coords = [
            ((n / NUMBER_POINTS) * (x2 - x1), y2) for n in range(1, NUMBER_POINTS + 1)
        ]

        right_coords = [
            (x3 + (n / NUMBER_POINTS) * (x4 - x3), y3) for n in range(NUMBER_POINTS)
        ]

        if self._gradient > GRADIENT_TOLERANCE:
            left_coords = left_coords[:-1]

        # add in 3 coordinates for the slope
        dx = (x3-x2)
        dy = (y2-y3)

        slope_sections = NUMBER_POINTS_SLOPE + 1

        if not deep_seeded_only:
            mid_coords = []

            for i in range(1, slope_sections):
                mid_coords.append(
                    (x2 + dx * i / slope_sections,
                    y2 - dy * i / slope_sections) 
                )

            # only want lines from mid to right for a not very steep gradient
            if self._gradient < GRADIENT_TOLERANCE:
                left_coords += mid_coords
            
            right_coords += mid_coords

        search = {}

        min_dist = dist_points(self._top_coord,self._bot_coord)/3

        # loop through left and right coordinates and generate a circular slope
        # that passes through these points
        # Not sure if multiprocessing can help, always made it slightly slower for all my tests

        for l_c in tqdm(left_coords):
            for r_c in right_coords:
                if dist_points(l_c,r_c) > min_dist and abs(l_c[0]-r_c[0])>0.1:
                    search.update(
                        self.run_analysis_for_circles(l_c, r_c, NUMBER_CIRCLES)
                    )

        self._search = search
        self._min_FOS_location = min(search, key=search.get)
        self._min_FOS = search[self._min_FOS_location]

    def run_analysis_for_circles(self, l_c : tuple , r_c : tuple, NUMBER_CIRCLES : float = 5) -> dict:
        """Runs slope analyse for fixed left and right points for
        a number of possible circular failures.

        Parameters
        ----------
        l_c : tuple,
            left coordinate written in the form (x,y)
        r_c : tuple
            right coordinate written in the form (x,y)
        NUMBER_CIRCLES : int, optional
            Number of circular slopes to break the area into
            (although some potential slopes might not be generated),
            by default 5

        Returns
        -------
        _type_
            _description_
        """

        #data validation
        assert_strictly_positive_number(NUMBER_CIRCLES,'NUMBER_CIRCLES')
        NUMBER_CIRCLES = int(NUMBER_CIRCLES)

        assert_length(l_c,2,'l_c')
        assert_length(r_c,2,'r_c')


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

            result = self.analyse_circular_failure(c_x, c_y, radius)
            if result:
                FOS,i_l,i_r = result
                search[(c_x,c_y,radius,i_l,i_r)] = FOS
            else:
                break

        return search

    def _reset_results(self):
        """ Re-initialise results to erase non-relevant results due to a model change"""
        self._search = {}
        self._min_FOS = 0
        self._slices = []   

    
    def plot_boundary(self):
        """Plot external boundary, materials, loading and water for model.

        Returns
        -------
        plotly figure

        """
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
        tot_l = self._external_length
        num_materials = len(self._materials)

        # loop through materials
        for i, m in enumerate(self._materials):
            # get reference level (y coordinate) for material
            y = m.RL

            if y <= self._bot_coord[1]:
                line = [(0,y),(self._external_length,y)]
            else:
                x = self._top_coord[0]+(self._top_coord[1]-y)/self._gradient
                line = [(0,y),(x,y)]

            # if the bot slope coordinate is between the bounds of the material
            # OR LAST material and above need to draw a bit differently

            is_last = (i == num_materials - 1)

            if ((top[1][1] > self._bot_coord[1] and
                line[1][1] < self._bot_coord[1]) or 
                (is_last and top[1][1]>self._bot_coord[1])):
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

        if self._load_magnitude:
            fig = self._plot_load(fig)
        
        if self._water_RL:
            fig = self._plot_water(fig)

        return fig

    def plot_critical(self):
        """Plot critical slope (ie slope with lowest FOS)

        Returns
        -------
        Plotly figure
        """
        fig = self.plot_boundary()

        c_x, c_y, radius, l_c,r_c = self._min_FOS_location
        FOS = self._min_FOS

        fig = self._plot_failure_plane(fig, c_x, c_y, radius, l_c,r_c,FOS=FOS, detailed=True)
        fig = self._plot_annotate_FOS(fig, c_x, c_y, FOS)
        return fig

    def _plot_annotate_FOS(self,fig,c_x,c_y,FOS):

        fig.add_trace(go.Scatter(
            x=[c_x],
            y=[c_y],
            mode="lines+text",
            text=[f"{FOS:.3f}"],
            textposition="top right",
            textfont=dict(
                family="sans serif",
                size=30,
                color="Green"
            )
        ))

        return fig

    def _plot_water(self,fig):
        if self._water_RL == None:
            return fig

        y = self._water_RL

        if y <= self._bot_coord[1]:
            x = [0,self._external_length]
        else:
            x = [0, self._top_coord[0]+(self._top_coord[1]-y)/self._gradient]
        
        fig.add_trace(
                go.Scatter(
                    x=x,
                    y=[y,y],
                    mode="lines",
                    line_color='blue',
                    line_width=4,
                )
            )

        fig.add_annotation(
            x=self._top_coord[0]/4,
            y=y,
            text='▼',
            showarrow=False,
            yshift=15,
            font_size=35,
            font_color='blue',
        )

        fig.add_annotation(
            x=self._top_coord[0]/4,
            y=y,
            text='_',
            showarrow=False,
            yshift=10,
            font_size=40,
            font_color='blue',
        )
        

        return fig

    def _plot_load(self,fig):
        # add in extra arrows, text, and hori line

        # arrow styling parameters
        ARROW_HEIGHT_FACTOR = 1.1
        arrowhead=3
        arrowsize=2
        arrowwidth=2
        arrowcolor='red'


        p = self._load_magnitude

        if p == 0:
            return fig

        y = self._external_height
        l_x,r_x = self._load_location

        # add more arrows in if the load is longer than say 3
        load_length = r_x - l_x

        if load_length > 3:
            spaces = divmod(load_length,1.5)[0]
            spacing = load_length/spaces
            arrows = [l_x + spacing * t for t in range(int(spaces+1))]
        else:
            arrows = [l_x,(l_x+r_x)/2,r_x]

        for x in arrows:
            fig.add_annotation(
                y = y,
                x = x,
                ay = y*ARROW_HEIGHT_FACTOR,
                ax = x + 0,
                text='',
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                showarrow = True,
                arrowhead=arrowhead,
                arrowsize=arrowsize,
                arrowwidth=arrowwidth,
                arrowcolor=arrowcolor,
            )

        fig.add_annotation(
            y = y*ARROW_HEIGHT_FACTOR,
            x = sum(self._load_location)/2,
            text=f'{p} kPa',
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow = False,
            font_size=30,
            yshift = 30,
            font_color=arrowcolor,
        )

        fig.add_annotation(
            y = y*ARROW_HEIGHT_FACTOR,
            x = l_x,
            ay = y*ARROW_HEIGHT_FACTOR,
            ax = r_x,
            text='',
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow = True,
            arrowhead=0,
            arrowsize=arrowsize,
            arrowwidth=arrowwidth,
            arrowcolor=arrowcolor,
        )

        return fig
    
    def _plot_failure_plane(self,fig,c_x,c_y,radius,l_c,r_c,FOS, detailed=False):
        if FOS > 3 :
            color = COLOUR_FOS_DICT[3.0]
        else:
            color = COLOUR_FOS_DICT[round(FOS,1)]

        # generate points for circle
        p = Point(c_x, c_y)
        x,y = p.buffer(radius).boundary.coords.xy
        
        x = list(x)
        y = list(y)

        # empty vectors for circle points that we will actually include
        x_ = []
        y_ = []

        for i in range(len(x)):
            # x coordinate should be between left and right
            # note for y, should be less than left y but can stoop
            # below right i
            if x[i] <= r_c[0] and x[i] >= l_c[0] and y[i] <= l_c[1]:
                x_.append(x[i])
                y_.append(y[i])
        
        if detailed:
            x_ += [l_c[0],c_x,r_c[0],x_[0]]
            y_ += [l_c[1],c_y,r_c[1],y_[0]]
        else:
            x_ = [r_c[0]] + x_ + [l_c[0]]
            y_ = [r_c[1]] + y_ + [l_c[1]]

        fig.add_trace(
            go.Scatter(
                x=x_,
                y=y_,
                mode="lines",
                line_color=color,
                meta = [round(FOS,3)],                
                hovertemplate="%{meta[0]}",
            )
        )

        return fig

    def plot_all_planes(self, max_fos=None):
        fig = self.plot_boundary()

        if max_fos is None:
            for k, v in self._search.items():
                c_x, c_y, radius, l_c,r_c = k
                fig = self._plot_failure_plane(fig, c_x, c_y, radius, l_c,r_c,FOS=v)
        else:
            for k, v in self._search.items():
                if v < max_fos:
                    c_x, c_y, radius, l_c,r_c = k
                    fig = self._plot_failure_plane(fig, c_x, c_y, radius, l_c,r_c,FOS=v)
                
                
        return fig



if __name__ == "__main__":
    s = Slope(height=2, angle=None, length=0.005)

    sand = Material(20,35,5,1)
    clay = Material(18,25,5,4)
    grass = Material(16,20,4,10)

    s.set_materials(sand,clay,grass)
    s.update_options(iterations=1200)
    s.set_water_table('5')

    s.set_surcharge(0.5,20,1)

    s.analyse_slope()

    f = s.plot_all_planes()

    print(len(s._search))
    

    # t1 = time.perf_counter()
    # s.analyse_slope()
    # print(
    #     f"Took {time.perf_counter()-t1} seconds to process {len(s._search.keys())} runs"
    # )
    # f = s.plot_all_planes()
    f.write_html('test.html')
