from math import radians


from math import radians, tan
from shapely.geometry import Polygon

import plotly.graph_objects as go



class Slope:
    def __init__(self, height=2, angle=30, length=None):
        
        self.height = height

        if length:
            self.length = length
        else:
            self.length = height / tan(radians(30))

        self._model_height = int(height * 4)
        self._model_length = int(length * 4)

        l, h = length, height

        self._external_boundary = Polygon([[0,0],[0,4*h],[2*l,4*h],[3*l,3*h],[5*l,3*h],[5*l,0],[0,0]])


if __name__ == "__main__":
    s = Slope(height=2, angle=None, length=2)
    x_, y_ = s._external_boundary.exterior.coords.xy
    fig = go.Figure(go.Scatter(x=list(x_), y=list(y_), fill="toself"))
    fig.show()