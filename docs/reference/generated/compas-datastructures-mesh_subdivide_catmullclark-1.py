from compas.datastructures.mesh import Mesh
from compas.visualization.plotters import MeshPlotter
from compas.datastructures.mesh.algorithms import mesh_subdivide_catmullclark

vertices = [[0., 0., 0.], [1., 0., 0.], [1., 1., 0.], [0., 1.0, 0.]]
faces = [[0, 1, 2, 3], ]

mesh = Mesh.from_vertices_and_faces(vertices, faces)
subd = mesh_subdivide_catmullclark(mesh, k=3, fixed=mesh.vertices())

plotter = MeshPlotter(subd)

plotter.draw_vertices(facecolor={key: '#ff0000' for key in mesh.vertices()}, radius=0.01)
plotter.draw_faces()

plotter.show()