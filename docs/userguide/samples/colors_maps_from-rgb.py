# type: ignore

from compas.geometry import Bezier, Point, Polygon, Vector
from compas.utilities import linspace, pairwise
from compas.datastructures import Mesh
from compas.colors import ColorMap
from compas_view2.app import App

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

viewer = App()
viewer.view.show_grid = False
viewer.add(mesh, facecolor=facecolors, show_lines=False)
viewer.show()
