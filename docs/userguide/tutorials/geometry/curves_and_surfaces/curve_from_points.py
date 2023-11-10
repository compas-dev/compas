from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import NurbsCurve
from compas.scene import SceneObject
from compas.colors import Color


points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -3, 3), Point(10, 0, 0)]

curve = NurbsCurve.from_points(points)

# ==============================================================================
# Visualisation
# ==============================================================================

SceneObject.clear()

SceneObject(curve).draw(color=Color.green())
SceneObject(Polyline(curve.points)).draw(show_points=True)

SceneObject.redraw()
