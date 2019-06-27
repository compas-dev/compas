from compas.datastructures import Mesh
from compas.datastructures import mesh_delete_duplicate_vertices
from compas_plotters import MeshPlotter

vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (10.0, 10.0, 0.0), (0.0, 10.0, 0.0), (5.0, 5.0, 0.0), (5.0, 5.0, 0.0)]
faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 5]]

mesh = Mesh.from_vertices_and_faces(vertices, faces)

plotter = MeshPlotter(mesh, figsize=(10, 7))

plotter.draw_edges()

print("Original mesh:")
print(mesh)

mesh_delete_duplicate_vertices(mesh)

print("Mesh with duplicate vertices deleted:")
print(mesh)

plotter.show()
