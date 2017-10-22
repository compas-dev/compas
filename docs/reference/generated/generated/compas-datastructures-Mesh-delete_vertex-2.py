import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.delete_vertex(17)
mesh.delete_vertex(18)
mesh.delete_vertex(0)
mesh.cull_vertices()

color = {key: '#ff0000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2}

plotter = MeshPlotter(mesh)
plotter.draw_vertices(facecolor=color)
plotter.draw_faces()
plotter.show()