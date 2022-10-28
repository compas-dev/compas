from math import radians

from compas.datastructures import Assembly
from compas.datastructures import Part
from compas.geometry import Box
from compas.geometry import Cylinder
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Frame

from compas_view2.app import App

assembly = Assembly()

a = Part(name="A", geometry=Box.from_width_height_depth(1, 1, 1))

b = Part(
    name="B",
    frame=Frame([0, 0, 1], [1, 0, 0], [0, 1, 0]),
    shape=Box.from_width_height_depth(1, 1, 1),
    features=[(Cylinder(Circle(Plane.worldXY(), 0.2), 1.0), "difference")],
)

b.transform(Rotation.from_axis_and_angle([0, 0, 1], radians(45)))
b.transform(Translation.from_vector([0, 0, 1]))

assembly.add_part(a)
assembly.add_part(b)

assembly.add_connection(a, b)

viewer = App()
viewer.add(b.geometry)
viewer.add(b.frame)
viewer.show()
