from compas.geometry import Vector, Point, Plane
from compas.geometry import Line, Polyline
from compas.geometry import Ellipse
from compas.utilities import pairwise
from compas.geometry import NurbsCurve
from compas.artists import Artist


ellipse = Ellipse(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 2.0, 1.0)
curve = NurbsCurve.from_ellipse(ellipse)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

Artist(Polyline(curve.locus())).draw()

for point in curve.points:
    Artist(point).draw()

for a, b in pairwise(curve.points):
    Artist(Line(a, b)).draw()

Artist.redraw()
