from compas.datastructures import Assembly
from compas.datastructures import Part
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Translation

# a block assembly

assembly = Assembly()

a = Part(name='A')
a.mesh = Mesh.from_shape(Box.from_width_height_depth(1, 1, 1))

b = Part(name='B')
b.mesh = Mesh.from_shape(Box.from_width_height_depth(1, 1, 1))
b.mesh.transform(Translation.from_vector([0, 0, 1]))

assembly.add_part(a)
assembly.add_part(b)

assembly.add_connection(a, b)

print(assembly)
print(assembly.find(a.guid))
