from math import radians

from compas.datastructures import Assembly
from compas.datastructures import Part
from compas.geometry import Box
from compas.geometry import Cylinder
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Translation
from compas.geometry import Transformation
from compas.geometry import Rotation
from compas.geometry import Frame

from compas_view2.app import App
from compas_view2.collections import Collection


class Block(Part):
    def get_geometry(self, _=False):
        transformation = Transformation.from_frame(self.frame)
        return Box.from_width_height_depth(1, 1, 1).transformed(transformation)


assembly = Assembly()

f1 = Frame([0, 0, 1], [1, 0, 0], [0, 1, 0])
f2 = f1.copy()
f2.transform(Rotation.from_axis_and_angle([0, 0, 1], radians(45)))
f2.transform(Translation.from_vector([0, 0, 1]))

a = Block(name="A", frame=f1)
b = Block(name="B", frame=f2)

assembly.add_part(a)
assembly.add_part(b)

assembly.add_connection(a, b)

viewer = App()
viewer.add(Collection(items=[a.get_geometry(), b.get_geometry(), a.frame, b.frame]))
viewer.show()
