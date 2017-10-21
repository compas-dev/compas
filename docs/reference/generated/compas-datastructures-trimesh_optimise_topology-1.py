from compas.datastructures import Mesh
from compas.visualization import MeshPlotter
from compas.datastructures import trimesh_optimise_topology

vertices = [
    (0.0, 0.0, 0.0),
    (10.0, 0.0, 0.0),
    (10.0, 10.0, 0.0),
    (0.0, 10.0, 0.0),
    (5.0, 5.0, 0.0)
]
faces = [
    (0, 1, 4),
    (1, 2, 4),
    (2, 3, 4),
    (3, 0, 4)
]

mesh = Mesh.from_vertices_and_faces(vertices, faces)

trimesh_optimise_topology(
    mesh,
    target=0.5,
    tol=0.05,
    kmax=300,
    allow_boundary_split=True,
    allow_boundary_swap=True,
    verbose=False
)

plotter = MeshPlotter(mesh)

plotter.draw_vertices(radius=0.05)
plotter.draw_faces()

plotter.show()