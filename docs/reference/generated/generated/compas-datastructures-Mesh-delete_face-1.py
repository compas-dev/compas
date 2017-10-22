import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.delete_face(12)

plotter = MeshPlotter(mesh)
plotter.draw_vertices()
plotter.draw_faces()
plotter.show()