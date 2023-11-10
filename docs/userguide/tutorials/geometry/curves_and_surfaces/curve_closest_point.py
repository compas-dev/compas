from compas.geometry import Point
from compas.geometry import NurbsCurve
from compas.scene import SceneObject
from compas.colors import Color


points = [Point(0, 0, 0), Point(3, 0, 2), Point(6, 0, -3), Point(8, 0, 0)]
curve = NurbsCurve.from_interpolation(points)

projection_point = Point(2, -1, 0)

closest_point, t = curve.closest_point(projection_point, return_parameter=True)

print(curve.point_at(t) == closest_point)

# ==============================================================================
# Visualisation
# ==============================================================================

SceneObject.clear()

SceneObject(curve, color=Color.from_hex("#0092D2")).draw()

SceneObject(projection_point).draw()
SceneObject(closest_point).draw()

SceneObject.redraw()
