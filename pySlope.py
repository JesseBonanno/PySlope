from math import radians, tan, sqrt, atan, cos, sin
from shapely.geometry import Polygon, LineString, Point, LinearRing, MultiPoint

import plotly.graph_objects as go

from dataclasses import dataclass

class Slope:
    def __init__(self, height=2, angle=30, length=None):
        
        self.height = height

        if length:
            self.length = length
        else:
            self.length = height / tan(radians(30))

        # set up external boundary as a shapely polygon, adopt a max height of 4* h and a max length of 5 * l
        l, h = length, height
        self._external_boundary = LinearRing([(0,0),(0,4*h),(3*l,4*h),(4*l,3*h),(7*l,3*h),(7*l,0),(0,0)])

        self._materials = []

        self._top_coord = [3*l, 4*h]
        self._bot_coord = [4*l, 3*h]
        self._gradient = h / l

        self._water_depth = None

        self._search = {}
        self._min_FOS = 0

    def add_water_table( self, depth : int = 1 ):
        self._water_depth = depth

    def remove_water_table(self):
        self._water_depth = None 

    def plot_boundary(self):
        x_, y_ = self._external_boundary.coords.xy
        fig = go.Figure(go.Scatter(x=list(x_), y=list(y_), fill="toself"))

        for m in self._materials:
                
            y = m.RL
            line = LineString([(-1,y),(self._external_boundary.bounds[2]+1,y)])
           
            x = self._external_boundary.intersection(line)
            # returns multipoint so convert to linestring as follows
            x = LineString(list(x))

            x_, y_ = x.coords.xy
            fig.add_trace(go.Scatter(x=list(x_),y=list(y_),mode='lines'))

        if self._search:
            for k,v in self._search.items():
                c_x,c_y,radius = k
                fig.add_shape(type="circle",
                    xref="x", yref="y",
                    x0=(c_x-radius), y0=(c_y-radius), x1=(c_x+radius), y1=(c_y+radius),
                    line_color="LightSeaGreen",
                )

        return fig

    def add_materials(self,*materials):

        for material in materials:
            if not isinstance(material, Material):
                raise ValueError('The funciton add_materials only accepts instances of the Material Class')

        l = [material.depth_to_bottom for material in materials]
        if len(l) > len(set(l)):
            raise ValueError('The same material depth has been input twice')

        # sort materials to be in order, include existing materials
        materials = list(materials) + self._materials
        materials.sort(key=lambda x: x.depth_to_bottom)

        # define RL for each material
        for material in materials:
            material.RL = self._top_coord[1] - material.depth_to_bottom

        self._materials = materials
        
    def remove_material(self,material=None, depth=None):
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
    
    def analyse_circular_failure(self, c_x,c_y,radius):
        # get circle for analysis, note circle is actually a 64 sided polygon (not exact but close enough for calc)
        #https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
        p = Point(c_x,c_y)
        c = p.buffer(radius).boundary

        # find intersection points with boundary if any, else return None
        if c.intersects(self._external_boundary):
            i = c.intersection(self._external_boundary)
        else:
            return None

        # list for intersecting points between circle and external boundary
        i_list = []

        # loop through each point in the intersection list
        for p in i.geoms:
            # if point append x,y to list
            if isinstance(p, Point):
                i_list.append((round(p.x,5),round(p.y,5)))

            # might actually give a line string of the tiniest length
            # could happen due to 64 sided polygon if the circle is close to intersecting
            # at its end. In this case just use the first point of the line
            # since the points are close together anyways
            elif isinstance(p, LineString):
                i_list.append(round(p.coords[0][0],5), round(p.coords[0][1],5))

        # make sure no input inside twice. Has been observed where the point of intersection
        # is the boundary between two linestrings
        i_list = list(set(i_list))

        # check that there are only two intersecting points otherwise something is wrong
        if len(i_list) != 2:
            return None
        
        # total number of slices
        SLICES = 50

        # horizontal distance between left and right slice
        dist = i_list[1][0] - i_list[0][0]

        # width of a slice
        b = dist / SLICES
        
        #initialise left point of first slice
        s_x = i_list[0][0] + b/2

        # intialise the push and resistance components for FOS before looping
        pushing = 0
        resisting = 0
        
        # loop through slice, actually want to iterate 1 time less than 
        # the number of slices since we start at half a slice
        for slice in range(1,SLICES):
            # define y coordinates for slice
            s_yb = c_y - sqrt(radius**2-(s_x-c_x)**2)
            
            #get y coordinate at top
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
                s_yt = ( - self._gradient ) * (s_x-self._top_coord[0]) + self._top_coord[1]
                                

            # get alpha, dy always positive, dx negative to right (uphill), dx positive to left
            # note alpha in radians by default
            dy = c_y - s_yb
            dx = c_x - s_x
            alpha = atan(dx/dy)

            # get height of unit
            h = s_yt - s_yb

            # get length
            l = b/cos(alpha)

            # intialize properties
            W = 0 #kN
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
                    W += b * m.unit_weight * (top-m.RL)
                    top = m.RL
                # in the case that the bottom of the strip is now outside the range
                # we still have material between the current top and the bottom of the strip
                # we capture it in this edge case and then break since everything below can be ignored
                # we also grab the material properties at the base
                else:
                    W += b * m.unit_weight * (top-s_yb)
                    top = m.RL
                    cohesion = m.cohesion
                    friction_angle = m.friction_angle
                    break

            # check case that ran out of layers (loop terminated earlier than expected)
            if top > s_yb:
                m = self._materials[-1]
                W += b * m.unit_weight * (top-s_yb)

            if self._water_depth:
                U = max(min(self._water_depth, s_yt)-s_yb,0) * 9.81
            else:
                U = 0
                
            resisting += cohesion*l + (W*cos(alpha)-U)*tan(friction_angle)
            pushing += W * sin(alpha)

            # initialise slice x coordinate for next loop
            s_x += b 

        return resisting / pushing

    def analyse_slope(self):
        
        total_searches = 100
        total_diameters = 5
        tp_xy = int(sqrt(total_searches / total_diameters))

        # select a bunch of points in a smart way
        x1,y1 = self._top_coord
        x2,y2 = self._bot_coord

        l = sqrt((x2-x1)**2 + (y1-y2)**2)

        max_radius = sqrt((x2-x1)**2 + (y1-y2)**2)
        search = {}

        for x in range(tp_xy):
            c_x = ( x1 + x2 ) / 2 + ( x + 0.2 ) * l / 4
            for y in range(tp_xy):
                c_y = y1 + (y ) * l / 4
                for r in range(total_diameters):
                    radius = 1.5 * l + r * (max_radius-1.5 *l)/total_diameters
                    FOS = self.analyse_circular_failure(c_x,c_y,radius)
                    if FOS:
                        search[(c_x,c_y,radius)] = self.analyse_circular_failure(c_x,c_y,radius)
                    else:
                        break

        self._search = search
        self._min_FOS = min(search, key=search.get)
        


@dataclass
class Material:
    unit_weight: float = 20
    friction_angle: int = 35
    cohesion: int = 2
    depth_to_bottom: int = 5

    def __repr__(self):
        return f'Material(uw={self.unit_weight},phi={self.friction_angle},c={self.cohesion},d_bot={self.depth_to_bottom}'


if __name__ == "__main__":
    s = Slope(height=2, angle=None, length=2)

    sand = Material(20,30,0,1)
    clay = Material(18,25,5,3)

    s.add_materials(sand,clay)
    s.analyse_slope()

    fig = s.plot_boundary()
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    fig.write_html("./test.html")
