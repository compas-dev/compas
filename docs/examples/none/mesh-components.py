from compas.datastructures import Mesh

vertices = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [2.0, 0.0, 0.0],
    [2.0, 0.0, 0.0],
    [3.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [1.0, 1.0, 0.0],
    [2.0, 1.0, 0.0],
    [2.0, 1.0, 0.0],
    [3.0, 1.0, 0.0],
]

faces = [
    [0, 1, 6, 5],
    [1, 2, 7, 6],
    [3, 4, 9, 8]
    ]

mesh = Mesh.from_vertices_and_faces(vertices, faces)

print(mesh_disconnected_vertices(mesh))
print(mesh_disconnected_faces(mesh))
print(mesh_explode(mesh))
