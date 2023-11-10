from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import NurbsSurface
from compas.scene import SceneObject


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

SceneObject.clear()

u = surface.u_isocurve(0.5 * sum(surface.u_domain))
v = surface.v_isocurve(0.5 * sum(surface.v_domain))

SceneObject(Polyline(u.locus())).draw()
SceneObject(Polyline(v.locus())).draw()

# for curve in surface.boundary():
#     Artist(Polyline(curve.locus())).draw()

SceneObject(other).draw()

SceneObject.redraw()
