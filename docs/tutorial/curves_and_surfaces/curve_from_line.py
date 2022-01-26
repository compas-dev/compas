from compas.geometry import Point
from compas.geometry import Line, Polyline
from compas.geometry import NurbsCurve
from compas.artists import Artist


line = Line(Point(0, 0, 0), Point(3, 3, 0))
curve = NurbsCurve.from_line(line)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

Artist(Polyline(curve.locus())).draw()

for point in curve.points:
    Artist(point).draw()

Artist.redraw()
