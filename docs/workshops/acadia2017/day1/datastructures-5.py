import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(text={key: '%.1f' % mesh.vertex_area(key) for key in mesh.vertices()})
plotter.draw_faces()
plotter.draw_edges()

plotter.show()