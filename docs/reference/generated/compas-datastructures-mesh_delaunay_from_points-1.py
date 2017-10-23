import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_delaunay_from_points

from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
faces = mesh_delaunay_from_points(vertices)

delaunay = Mesh.from_vertices_and_faces(vertices, faces)

plotter = MeshPlotter(delaunay)

plotter.draw_vertices(radius=0.1)
plotter.draw_faces()

plotter.show()