import compas
from compas.datastructures import Mesh

vertices = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0]
]

faces = [
    [0, 1, 2]
]

mesh = Mesh.from_vertices_and_faces(vertices, faces)
print(trimesh_face_circle(mesh, 0))
