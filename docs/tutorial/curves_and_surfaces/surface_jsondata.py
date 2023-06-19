from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import NurbsSurface
from compas.artists import Artist


points = [
    [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0)],
    [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0)],
    [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0)],
    [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0)],
]

surface = NurbsSurface.from_points(points=points)

# ==============================================================================
# JSON Data
# ==============================================================================

string = surface.to_jsonstring(pretty=True)

print(string)

other = NurbsSurface.from_jsonstring(string)

# print(surface == other)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

u = surface.u_isocurve(0.5 * sum(surface.u_domain))
v = surface.v_isocurve(0.5 * sum(surface.v_domain))

Artist(Polyline(u.locus())).draw()
Artist(Polyline(v.locus())).draw()

# for curve in surface.boundary():
#     Artist(Polyline(curve.locus())).draw()

Artist(other).draw()

Artist.redraw()
