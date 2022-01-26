from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import NurbsCurve
from compas.artists import Artist


points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -3, 3), Point(10, 0, 0)]

curve = NurbsCurve.from_points(points)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

Artist(Polyline(curve.locus())).draw()
Artist(Polyline(curve.points)).draw()

Artist.redraw()
