from numpy import array

from math import pi
from compas.utilities import print_profile
from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.datastructures import Mesh
from compas.datastructures import mesh_transform_numpy

mesh_transform_numpy = print_profile(mesh_transform_numpy)

box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

T = Translation([-2.0, 0.0, 3.0])
R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], pi / 2)

T = array(T)
R = array(R)

M = R.dot(T)

mesh_transform_numpy(mesh, M)

print(mesh.get_vertices_attribute('x'))
