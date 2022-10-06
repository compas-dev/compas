from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import NurbsSurface
from compas.artists import Artist


points = [
    [
        Point(0, 0, 0),
        Point(1, 0, +0),
        Point(2, 0, +0),
        Point(3, 0, +0),
        Point(4, 0, +0),
        Point(5, 0, 0),
    ],
    [
        Point(0, 1, 0),
        Point(1, 1, -1),
        Point(2, 1, -1),
        Point(3, 1, -1),
        Point(4, 1, -1),
        Point(5, 1, 0),
    ],
    [
        Point(0, 2, 0),
        Point(1, 2, -1),
        Point(2, 2, +2),
        Point(3, 2, +2),
        Point(4, 2, -1),
        Point(5, 2, 0),
    ],
    [
        Point(0, 3, 0),
        Point(1, 3, -1),
        Point(2, 3, +2),
        Point(3, 3, +2),
        Point(4, 3, -1),
        Point(5, 3, 0),
    ],
    [
        Point(0, 4, 0),
        Point(1, 4, -1),
        Point(2, 4, -1),
        Point(3, 4, -1),
        Point(4, 4, -1),
        Point(5, 4, 0),
    ],
    [
        Point(0, 5, 0),
        Point(1, 5, +0),
        Point(2, 5, +0),
        Point(3, 5, +0),
        Point(4, 5, +0),
        Point(5, 5, 0),
    ],
]

weights = [
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
]

surface = NurbsSurface.from_parameters(
    points=points,
    weights=weights,
    u_knots=[
        1.0,
        1 + 1 / 9,
        1 + 2 / 9,
        1 + 3 / 9,
        1 + 4 / 9,
        1 + 5 / 9,
        1 + 6 / 9,
        1 + 7 / 9,
        1 + 8 / 9,
        2.0,
    ],
    v_knots=[0.0, 1 / 9, 2 / 9, 3 / 9, 4 / 9, 5 / 9, 6 / 9, 7 / 9, 8 / 9, 1.0],
    u_mults=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    v_mults=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    u_degree=3,
    v_degree=3,
)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

for row in surface.points:
    Artist(Polyline(row)).draw()

for col in zip(*list(surface.points)):
    Artist(Polyline(col)).draw()

Artist(surface).draw()

Artist.redraw()
