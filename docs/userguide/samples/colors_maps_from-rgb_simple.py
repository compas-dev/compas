# type: ignore

from compas.geometry import Point, Polygon
from compas.utilities import linspace, pairwise
from compas.datastructures import Mesh
from compas.colors import ColorMap
from compas_view2.app import App

n = 256
t = 0.3

up = []
down = []
for i in linspace(0, 10, n):
    point = Point(i, 0, 0)
    up.append(point + [0, t, 0])
    down.append(point - [0, t, 0])

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
