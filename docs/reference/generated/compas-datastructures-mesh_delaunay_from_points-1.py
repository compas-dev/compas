import compas
from compas.datastructures.mesh import Mesh
from compas.visualization.plotters import MeshPlotter
from compas.datastructures.mesh.algorithms import mesh_delaunay_from_points

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

vertices = [mesh.vertex_coordinates(key) for key in mesh]
faces = mesh_delaunay_from_points(vertices)

delaunay = Mesh.from_vertices_and_faces(vertices, faces)

plotter = MeshPlotter(delaunay)

plotter.draw_vertices(radius=0.1)
plotter.draw_faces()

plotter.show()