from compas.geometry import Vector, Point, Plane
from compas.geometry import Polyline
from compas.geometry import Circle
from compas.geometry import NurbsCurve
from compas.artists import Artist
from compas.colors import Color


circle = Circle(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 1.0)
curve = NurbsCurve.from_circle(circle)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

Artist(curve).draw(color=Color.green())
Artist(Polyline(curve.points)).draw(show_points=True)

Artist.redraw()
