# type: ignore

from compas_viewer import Viewer

from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Polygon
from compas.utilities import linspace
from compas.utilities import pairwise

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

viewer = Viewer(show_grid=False)
viewer.scene.add(mesh, facecolor=facecolors, show_lines=False, show_points=False)
viewer.show()
