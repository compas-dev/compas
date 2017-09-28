import compas
from compas.datastructures import Mesh
from compas.visualization.plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(radius=0.2)
plotter.draw_faces()
plotter.show()