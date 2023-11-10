from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import NurbsCurve
from compas.scene import SceneObject
from compas.colors import Color


line = Line(Point(0, 0, 0), Point(3, 3, 0))
curve = NurbsCurve.from_line(line)

# ==============================================================================
# Visualisation
# ==============================================================================

SceneObject.clear()

SceneObject(curve).draw(color=Color.green())

for point in curve.points:
    SceneObject(point).draw()

SceneObject.redraw()
