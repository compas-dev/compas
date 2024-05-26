# type: ignore

from compas_viewer import Viewer

from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Bezier
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector
from compas.itertools import linspace
from compas.itertools import pairwise

n = 5000

zaxis = Vector.Zaxis()

points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -6, 0), Point(9, 0, 0)]
curve = Bezier(points)

up = []
down = []
for i in linspace(0, 1, n):
    point = curve.point_at(i)
    tangent = curve.tangent_at(i)
    normal = zaxis.cross(tangent)
    up.append(point + normal * 0.1)
    down.append(point - normal * 0.1)

polygons = []
for (d, c), (a, b) in zip(pairwise(up), pairwise(down)):
    polygons.append(Polygon([a, b, c, d]))

cmap = ColorMap.from_rgb()

mesh = Mesh.from_polygons(polygons)
facecolors = {i: cmap(i, minval=0, maxval=n - 1) for i in range(n)}

viewer = Viewer(show_grid=False)
viewer.scene.add(mesh, facecolor=facecolors, show_lines=False, show_points=False)
viewer.show()
