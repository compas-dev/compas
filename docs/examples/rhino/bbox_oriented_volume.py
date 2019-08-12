from compas.geometry import bounding_box
from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas.geometry import Rotation
from compas.remote import Proxy
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas.datastructures import mesh_unify_cycles
from random import random

proxy = Proxy()
proxy.module = 'numpy.random'

points = proxy.rand(100, 3)
points.append([0.0,0.0,0.0])
points.append([1.0,0.0,0.0])
points.append([1.0,1.0,0.0])
points.append([0.0,1.0,0.0])
points.append([0.0,0.0,1.0])
points.append([1.0,0.0,1.0])
points.append([1.0,1.0,1.0])
points.append([0.0,1.0,1.0])
points = [[x * 10, y, z * 3] for x, y, z in points]

bbox = bounding_box(points)
a = length_vector(subtract_vectors(bbox[1], bbox[0]))
b = length_vector(subtract_vectors(bbox[3], bbox[0]))
c = length_vector(subtract_vectors(bbox[4], bbox[0]))
v1 = a * b * c

proxy.module = 'compas.geometry'

R = Rotation.from_axis_and_angle([1.0, 1.0, 0.0], random() * 3.14159)
points = proxy.transform_points_numpy(points, R.matrix)

bbox = proxy.oriented_bounding_box_numpy(points)

a = length_vector(subtract_vectors(bbox[1], bbox[0]))
b = length_vector(subtract_vectors(bbox[3], bbox[0]))
c = length_vector(subtract_vectors(bbox[4], bbox[0]))
v2 = a * b * c

print(v1, v2)

faces = [
    [3, 2, 1, 0],
    [0, 1, 5, 4],
    [1, 2, 6, 5],
    [2, 3, 7, 6],
    [3, 0, 4, 7],
    [4, 5, 6, 7]]

mesh = Mesh.from_vertices_and_faces(bbox, faces)
mesh_unify_cycles(mesh, root=0)

artist = MeshArtist(mesh)
artist.clear_layer()
artist.draw_points([{'pos': xyz} for xyz in points])
artist.draw_vertices()
artist.draw_edges()
artist.draw_mesh()
