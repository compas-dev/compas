from compas.datastructures import Mesh
from compas.datastructures import mesh_smooth_area

from compas_plotters import MeshPlotter


vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (6.0, 10.0, 0.0), (0.0, 10.0, 0.0)]
faces = [[0, 1, 2, 3]]

mesh = Mesh.from_vertices_and_faces(vertices, faces)

key = mesh.insert_vertex(0)
fixed = [key]

plotter = MeshPlotter(mesh, figsize=(10, 7))

plotter.draw_edges(width=0.5)

def callback(mesh, k, args):
    print(k)
    plotter.update_edges()
    plotter.update()

trimesh_remesh(
    mesh,
    0.5,
    kmax=200,
    allow_boundary_split=True,
    allow_boundary_swap=True,
    allow_boundary_collapse=True,
    fixed=fixed,
    callback=callback)

mesh_smooth_area(mesh, fixed=mesh.vertices_on_boundary())

plotter.update_edges()
plotter.update(pause=2.0)
plotter.show()