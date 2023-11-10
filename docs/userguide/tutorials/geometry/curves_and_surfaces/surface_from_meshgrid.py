from compas.geometry import Point
from compas.geometry import Polyline
from compas.utilities import meshgrid, linspace
from compas.geometry import NurbsSurface
from compas.scene import SceneObject


UU, VV = meshgrid(linspace(0, 8, 9), linspace(0, 5, 6))

Z = 0.5

points = []
for i, (U, V) in enumerate(zip(UU, VV)):
    row = []
    for j, (u, v) in enumerate(zip(U, V)):
        if i == 0 or i == 5 or j == 0 or j == 8:
            z = 0.0
        elif i < 2 or i > 3:
            z = -1.0
        else:
            if j < 2 or j > 6:
                z = -1.0
            else:
                z = Z
        row.append(Point(u, v, z))
    points.append(row)

surface = NurbsSurface.from_points(points=points)

# ==============================================================================
# Visualisation
# ==============================================================================

SceneObject.clear()

for row in surface.points:
    SceneObject(Polyline(row)).draw()

for col in zip(*list(surface.points)):
    SceneObject(Polyline(col)).draw()

SceneObject(surface).draw()

SceneObject.redraw()
