import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(text='key')
plotter.draw_edges()
plotter.draw_faces()

plotter.show()