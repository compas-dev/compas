from compas.utilities import linspace
from compas.geometry import Point, Vector, Frame
from compas.geometry import Line, Circle, Ellipse, Arc, Polyline, Bezier, NurbsCurve
from compas_view2.app import App

controlcircle = Circle(1.0, frame=Frame([0, 0, 0], [0, 1, 0], [0, 0, 1]))
controlpoints = []
for t in linspace(0, 2, 21):
    x = t * 5
    _, y, z = controlcircle.point_at(t)
    point = Point(x, y, z)
    controlpoints.append(point)

controlpoly = Polyline(controlpoints)
curve = Bezier(controlpoints)

# =============================================================================
# Viz
# =============================================================================

viewer = App()

viewer.add(curve.to_polyline(n=1000), linewidth=3)
viewer.add(controlpoly, linewidth=0.5, pointsize=5, show_points=True)


@viewer.on(interval=100, frames=101)
def slide(f):
    t = f / 100

    point = curve.point_at(t=t)
    normal = curve.normal_at(t=t)
    frame = curve.frame_at(t=t)
    circle = Circle(radius=0.2, frame=Frame(frame.point, frame.yaxis, frame.zaxis))

    if normal is not None:
        normal = Line.from_point_and_vector(point, normal * 0.1)
        viewer.add(normal, linewidth=2)
        viewer.add(circle.to_polyline(100), linewidth=0.5)
        viewer.add(circle.point_at(t), pointcolor=(1, 0, 0))
        viewer.add(circle.point_at(0.33 + t), pointcolor=(0, 1, 0))
        viewer.add(circle.point_at(0.66 + t), pointcolor=(0, 0, 1))


viewer.run()
