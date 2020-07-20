import compas
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(text='key', radius=0.15)
plotter.draw_edges()
plotter.draw_faces()

plotter.show()