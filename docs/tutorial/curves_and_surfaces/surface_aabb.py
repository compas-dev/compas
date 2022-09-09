from math import radians
from compas.geometry import Point, Translation, Rotation
from compas.geometry import Polyline
from compas.geometry import NurbsSurface
from compas.artists import Artist


points = [
    [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0), Point(4, 0, 0)],
    [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0), Point(4, 1, 0)],
    [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0), Point(4, 2, 0)],
    [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0), Point(4, 3, 0)],
]

surface = NurbsSurface.from_points(points=points)

T = Translation.from_vector([0, -1.5, 0])
R = Rotation.from_axis_and_angle([0, 0, 1], radians(45))

surface.transform(R * T)

# ==============================================================================
# AABB
# ==============================================================================

box = surface.aabb(optimal=True)

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

for row in surface.points:
    Artist(Polyline(row)).draw()

for col in zip(*list(surface.points)):
    Artist(Polyline(col)).draw()

Artist(surface).draw()
Artist(box).draw()

Artist.redraw()
