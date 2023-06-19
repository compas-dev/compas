from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import NurbsCurve
from compas.artists import Artist
from compas.colors import Color


line = Line(Point(0, 0, 0), Point(3, 3, 0))
curve = NurbsCurve.from_line(line)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

Artist(curve).draw(color=Color.green())

for point in curve.points:
    Artist(point).draw()

Artist.redraw()
