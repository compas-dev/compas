# type: ignore

from compas.geometry import Pointcloud, Circle, Frame, Polygon
from compas.datastructures import Mesh
from compas.colors import Color, ColorMap
from compas_view2.app import App

viewer = App()
viewer.view.show_grid = False

cmap = ColorMap.from_mpl("viridis")
w = 16
h = 10
n = len(cmap.colors)
d = w / n
cloud = Pointcloud.from_bounds(w, h, 0, n)
white = Color.white()
facecolors = {}
polygons = []
for i, color in enumerate(cmap.colors):
    c = Circle(0.1, Frame(cloud[i]))
    p = Polygon(
        [
            [i * d, -2, 0],
            [(i + 1) * d, -2, 0],
            [(i + 1) * d, -1, 0],
            [i * d, -1, 0],
        ]
    )
    polygons.append(p)
    facecolors[i] = color
    viewer.add(c.to_polygon(100), facecolor=color)

viewer.add(Mesh.from_polygons(polygons), facecolor=facecolors, show_lines=False)

viewer.run()
