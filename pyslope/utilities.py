# standard library imports
from math import cos, sin, sqrt, radians
from colour import Color

MATERIAL_COLORS = [
    "#efa59c",
    "#77e1ca",
    "#cdacfc",
    "#f2c6a7",
    "#7edff4",
    "#f2a8c3",
    "#cde9ba",
    "#f2c1fa",
    "#f1dba3",
    "#a3acf7",
]


def is_color(color):
    try:
        color = Color(color)
        return True
    except ValueError:
        return False


def mid_coord(p1: tuple, p2: tuple) -> tuple:
    return [(a + b) / 2 for a, b in zip(p1, p2)]


def dist_points(p1: tuple, p2: tuple) -> float:
    return sqrt(abs(p1[0] - p2[0]) ** 2 + abs(p1[1] - p2[1]) ** 2)


def circle_radius_from_abcd(c_to_e, C):
    # two intersecting chords through circle have segments of chords related
    # as a * b = c * d , where a and b are the lengths of chord on each side of intersection
    # as such we have half_coord_distance ** 2 = chord_to_edge * (R + (R-chord_to_edge)) = C

    return (C + c_to_e**2) / (2 * c_to_e)


def circle_centre(beta, chord_intersection, chord_to_centre):
    dy = cos(beta) * chord_to_centre
    dx = sin(beta) * chord_to_centre

    return [a + b for a, b in zip(chord_intersection, (dx, dy))]


def cirle_line_intersection(top_coord, bot_coord, cx, cy, r):
    # Based on https://mathworld.wolfram.com/Circle-LineIntersection.html
    #  shift so 0,0 is datum
    top_coord = [(top_coord[0] - cx), (top_coord[1] - cy)]
    bot_coord = [(bot_coord[0] - cx), (bot_coord[1] - cy)]

    dx = bot_coord[0] - top_coord[0]
    dy = bot_coord[1] - top_coord[1]
    dr = sqrt(dx**2 + dy**2)

    D = top_coord[0] * bot_coord[1] - bot_coord[0] * top_coord[1]

    disc = abs(r**2 * dr**2) - abs(D**2)

    if disc < 0:
        return []

    if dy < 0:
        m = -1
    else:
        m = 1

    x1 = (D * dy + m * dx * sqrt(disc)) / dr**2 + cx
    x2 = (D * dy - m * dx * sqrt(disc)) / dr**2 + cx

    y1 = ((-(D * dx)) + abs(dy) * sqrt(disc)) / dr**2 + cy
    y2 = ((-(D * dx)) - abs(dy) * sqrt(disc)) / dr**2 + cy

    if disc == 0:
        return [(x1, y1)]
    else:
        return [(x1, y1), (x2, y2)]


def generate_circle_coordinates(c_x, c_y, radius, number_points=90):
    """Generate coordinates around bottom half of circumference of circle.

    Parameters
    ----------
    c_x : float
        circle centre x coordinate
    c_y : float
        circle centre y coordinate
    radius : float
        circle radius

    returns
    list of x coordinates and list of y coordinates.
    """

    x = [
        round(c_x - cos(radians(alpha)) * radius, 3)
        for alpha in range(1, 180, int(180 / number_points))
    ]
    y = [
        round(c_y - sin(radians(alpha)) * radius, 3)
        for alpha in range(1, 180, int(180 / number_points))
    ]

    return (x, y)


def create_fos_color_dictionary():
    colors = [
        (0, "red"),
        (1, "orange"),
        (2, "green"),
        (3, "#0c84a8"),
        (4, "#0c1ea8"),
        (5, "purple"),
    ]

    colors.sort(key=lambda x: x[0])

    color_dict = {}

    for i in range(len(colors) - 1):
        c1 = Color(colors[i][1])
        c2 = Color(colors[i + 1][1])

        p1 = colors[i][0]
        p2 = colors[i + 1][0]

        d = int((p2 - p1) * 10)

        color_range = list(c1.range_to(c2, d + 1))

        for f in range(d + 1):
            color_dict[round(f / 10 + p1, 1)] = color_range[f].hex

    return color_dict


COLOUR_FOS_DICT = create_fos_color_dictionary()


def get_precision(n):
    # determine the precision of the value entered
    mag = str(n)
    if "." not in mag:
        return 0
    else:
        decimals = mag.split(".")[1]
        for i in range(len(decimals) - 3):
            if decimals[i] == decimals[i + 1] == decimals[i + 2] == "0":
                return i

    return len(decimals)


def draw_line(
    fig,
    angle,
    x_sup,
    y_sup,
    length=-20,
    xoffset=0,
    yoffset=0,
    color="red",
    line_width=2,
):
    """Draw an anchored line on a plotly figure.

    Parameters
    ----------
    fig : plotly figure
        plotly figure to append line shape to.
    angle : int
        Angle of the line from the x-axis. Angle uses standard mathematical
        cartesian convention.
    x_sup : int
        The x position for the line to be anchored to.
    length : int, optional
        the line length, by default -20
    xoffset : int, optional
        The x-offset of the start of the line from the anchor, by default 0
    yoffset : int, optional
        The y-offset of the start of the line from the anchor, by default 0
    color : str, optional
        Line color, by default 'red'
    line_width : int, optional
        Line width, by default 2

    Returns
    -------
    plotly figure
        Returns the plotly figure passed into function with the arrowhead
        appended to it.
    """
    # Establish line start and end coordinates.
    x0 = xoffset
    y0 = yoffset
    x1 = x0 + int(length * cos(radians(angle)))
    y1 = y0 + int(length * sin(radians(angle)))

    # Create dictionary for shape object representing line.
    shape = dict(
        type="line",
        xref="x",
        yref="y",
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        line_color=color,
        line_width=line_width,
        xsizemode="pixel",
        ysizemode="pixel",
        xanchor=x_sup,
        yanchor=y_sup,
    )

    # Append shape to plot or subplot
    fig.add_shape(shape)

    return fig


def draw_arrowhead(
    fig, angle, x_sup, y_sup, length=5, xoffset=0, yoffset=0, color="red", line_width=2
):
    """Draw an anchored arrowhead on a plotly figure.

    Parameters
    ----------
    fig : plotly figure
        plotly figure to append arrowhead shape to.
    angle : int
        Angle of the arrowhead from the x-axis. Angle uses standard
        mathematical cartesian convention.
    x_sup : int
        The x position for the arrowhead to be anchored to.
    length : int, optional
        the arrowhead length, by default 5
    xoffset : int, optional
        The x-offset of the start of the arrowhead from the anchor, by
        default 0
    yoffset : int, optional
        The y-offset of the start of the arrowhead from the anchor, by
        default 0
    color : str, optional
        arrowhead color, by default 'red'
    line_width : int, optional
        Line width, by default 2
    row : int or None,
        Row of subplot to draw line on. If None specified assumes a full plot,
        by default None.
    col : int or None,
        Column of subplot to draw line on. If None specified assumes a full
        plot, by default None.

    Returns
    -------
    plotly figure
        Returns the plotly figure passed into function with the arrowhead
        appended to it.
    """
    # Holds lines 90 degrees apart to represent arrowhead. Constructed so 0
    # degrees is pointing right, follows conventions in documentation for angle

    # Angle conversion to allow for compatability with draw_line function
    a1 = 225 + angle
    a2 = 135 + angle

    # Append line to figure (half of arrowhead)
    fig = draw_line(
        fig,
        angle=a1,
        x_sup=x_sup,
        y_sup=y_sup,
        length=length,
        xoffset=xoffset,
        yoffset=yoffset,
        color=color,
        line_width=line_width,
    )

    # Append line to figure (half of arrowhead)
    fig = draw_line(
        fig,
        angle=a2,
        x_sup=x_sup,
        y_sup=y_sup,
        length=length,
        xoffset=xoffset,
        yoffset=yoffset,
        color=color,
        line_width=line_width,
    )

    return fig


def draw_arrow(
    fig,
    angle,
    force,
    x_sup,
    y_sup,
    xoffset=0,
    yoffset=0,
    color="red",
    line_width=2,
    arrowhead=5,
    arrowlength=40,
    show_values=True,
    units="N",
    precision=3,
):
    """Draw an anchored arrow on a plotly figure.

    Parameters
    ----------
    fig : plotly figure
        plotly figure to append arrow shape to.
    angle : int
        Angle of the arrow from the x-axis. Angle uses standard
        mathematical cartesian convention.
    force: int
        force that the arrow will represent. Only need to know whether it
        is positive or negative, but it generally is easiest to just parse
        the whole force in.
    x_sup : int
        The x position for the arrow to be anchored to.
    xoffset : int, optional
        The x-offset of the start of the arrow from the anchor, by default 0
    yoffset : int, optional
        The y-offset of the start of the arrow from the anchor, by default 0
    color : str, optional
        arrow color, by default 'red'
    line_width : int, optional
        Line width, by default 2
    arrowhead : int, optional
        Size of the arrowhead lines, by default 5
    arrowlength: int, optional
        length of the arrow line, by default 30
    show_values: bool,optional
        If true annotates numerical force value next to arrow, by default True.
    row : int or None,
        Row of subplot to draw line on. If None specified assumes a full plot,
        by default None.
    col : int or None,
        Column of subplot to draw line on. If None specified assumes a full
        plot, by default None.
    units: str,
        The units suffix drawn with the force value.
    precision: int,
        The decimal precision to be displayed for annotations, by default 3.

    Returns
    -------
    plotly figure
        Returns the plotly figure passed into function with the arrow
        appended to it.
    """
    # get precision as p
    p = precision

    # Factor to switch arrow direction based on force sign
    if force > 0:
        d = 1
    elif force < 0:
        d = -1
    else:
        return fig

    # Draw arrowhead for force
    fig = draw_arrowhead(
        fig,
        angle,
        x_sup,
        y_sup,
        length=arrowhead * d,
        xoffset=xoffset,
        yoffset=yoffset,
        color=color,
        line_width=line_width,
    )

    # Draw arrowline for force
    fig = draw_line(
        fig,
        angle,
        x_sup,
        y_sup,
        length=-1 * arrowlength * d,
        xoffset=xoffset,
        yoffset=yoffset,
        color=color,
        line_width=line_width,
    )

    if show_values:
        # determine start and end of arrow
        x0 = xoffset + x_sup
        y0 = yoffset + y_sup
        x1 = (int(-arrowlength * d * cos(radians(angle)))) * 1.1
        y1 = (int(-arrowlength * d * sin(radians(angle)))) * 1.3

        # make so text doesnt intersect x axis
        if abs(y1) < 5:
            if y1 >= 0:
                y1 = 10
            else:
                y1 = -10

        annotation = dict(
            xref="x",
            yref="y",
            x=x0,
            y=y0,
            xshift=x1,
            yshift=y1,
            text=f"{force:.{p}f} {units}",
            showarrow=False,
            font=dict(family="sans serif", size=20, color=color),
        )

        # Append shape to plot or esubplot
        fig.add_annotation(annotation)

    return fig
