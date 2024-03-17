# type: ignore

from compas_viewer import Viewer

from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Translation
from compas.utilities import linspace
from compas.utilities import pairwise

n = 1000
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

mesh = Mesh.from_polygons(polygons)

viewer = Viewer(show_grid=False)

cmap = ColorMap.from_two_colors(Color.from_hex("#0092d2"), Color.pink())
facecolors = {i: cmap(i, minval=0, maxval=n - 1) for i in range(n)}

viewer.scene.add(mesh, facecolor=facecolors, show_lines=False, show_points=False)

cmap = ColorMap.from_two_colors(Color.from_hex("#0092d2"), Color.pink(), diverging=True)
facecolors = {i: cmap(i, minval=0, maxval=n - 1) for i in range(n)}

translation = Translation.from_vector([0, -3 * t, 0])
viewer.scene.add(mesh.transformed(translation), facecolor=facecolors, show_lines=False, show_points=False)

viewer.show()
