from compas.geometry import Point
from compas.geometry import Polyline, Bezier
from compas.geometry import NurbsCurve
from compas.artists import Artist
from compas.colors import Color


points = [Point(0, 0, 0), Point(1, 3, 0), Point(2, 0, 0)]
bezier = Bezier(points)

points = [Point(3, 0, 0), Point(4, 3, 0), Point(5, 0, 0)]

curve1 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 1.0, 1.0],
    knots=[0.0, 1.0],
    multiplicities=[3, 3],
    degree=2,
)

curve2 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 2.0, 1.0],
    knots=[0.0, 1.0],
    multiplicities=[3, 3],
    degree=2,
)

curve3 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 1.0, 1.0],
    knots=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
    multiplicities=[1, 1, 1, 1, 1, 1],
    degree=2,
)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

Artist(Polyline(bezier.points)).draw()
Artist(Polyline(bezier.locus())).draw(show_points=True)

Artist(Polyline(curve1.points)).draw(show_points=True)

Artist(curve1).draw(color=Color.black())
Artist(curve2).draw(color=Color.pink())
Artist(curve3).draw(color=Color.azure())

Artist.redraw()
