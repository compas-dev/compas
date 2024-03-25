# type: ignore

from compas_viewer import Viewer

from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Pointcloud
from compas.geometry import Polygon

viewer = Viewer(show_grid=False)

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
    # c = Circle(0.1, Frame(cloud[i]))
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
    # viewer.add(c.to_polygon(100), facecolor=color)

viewer.scene.add(Mesh.from_polygons(polygons), facecolor=facecolors, show_lines=False, show_points=False)

viewer.show()
