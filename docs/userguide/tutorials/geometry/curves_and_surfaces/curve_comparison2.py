from compas.geometry import Point
from compas.geometry import Polyline, Bezier
from compas.geometry import NurbsCurve
from compas.scene import SceneObject
from compas.colors import Color


points = [Point(0, 0, 0), Point(1, 2, 0), Point(2, -2, 0), Point(3, 0, 0)]
bezier = Bezier(points)

points = [Point(4, 0, 0), Point(5, 2, 0), Point(6, -2, 0), Point(7, 0, 0)]

curve1 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 1.0, 1.0, 1.0],
    knots=[0.0, 1.0],
    multiplicities=[4, 4],
    degree=3,
)

curve2 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 2.0, 2.0, 1.0],
    knots=[0.0, 1.0],
    multiplicities=[4, 4],
    degree=3,
)

curve3 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 1.0, 1.0, 1.0],
    knots=[0.0, 1 / 3, 2 / 3, 1.0],
    multiplicities=[3, 1, 1, 3],
    degree=3,
)

curve4 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 1.0, 1.0, 1.0],
    knots=[0.0, 1 / 5, 2 / 5, 3 / 5, 4 / 5, 1.0],
    multiplicities=[2, 1, 1, 1, 1, 2],
    degree=3,
)

curve5 = NurbsCurve.from_parameters(
    points=points,
    weights=[1.0, 1.0, 1.0, 1.0],
    knots=[0.0, 1 / 7, 2 / 7, 3 / 7, 4 / 7, 5 / 7, 6 / 7, 1.0],
    multiplicities=[1, 1, 1, 1, 1, 1, 1, 1],
    degree=3,
)

# curve6 = NurbsCurve.from_parameters(
#     points=points,
#     weights=[1.0, 1.0, 1.0, 1.0],
#     knots=[0.0, 0.5, 1.0],
#     multiplicities=[3, 1, 3],
#     degree=2
# )

# ==============================================================================
# Visualisation
# ==============================================================================

SceneObject.clear()

SceneObject(Polyline(bezier.points)).draw()
SceneObject(Polyline(bezier.locus())).draw()

SceneObject(Polyline(curve1.points)).draw(show_points=True)

color = Color.red()

SceneObject(curve1).draw(color=color)
SceneObject(curve2).draw(color=color.lightened(factor=20))
SceneObject(curve3).draw(color=color.lightened(factor=40))
SceneObject(curve4).draw(color=color.lightened(factor=60))
SceneObject(curve5).draw(color=color.lightened(factor=80))
# Artist(curve6).draw(color=color.lightened(factor=50))

SceneObject.redraw()
