from compas.geometry import Vector, Point, Plane
from compas.geometry import Polyline
from compas.geometry import Ellipse
from compas.geometry import NurbsCurve
from compas.scene import SceneObject
from compas.colors import Color


ellipse = Ellipse(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 2.0, 1.0)
curve = NurbsCurve.from_ellipse(ellipse)

# ==============================================================================
# Visualisation
# ==============================================================================

SceneObject.clear()

SceneObject(curve).draw(color=Color.green())
SceneObject(Polyline(curve.points)).draw(show_points=True)

SceneObject.redraw()
