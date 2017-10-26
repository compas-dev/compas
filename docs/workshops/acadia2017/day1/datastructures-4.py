import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices()
plotter.draw_faces(text={fkey: '%.1f' % mesh.face_area(fkey) for fkey in mesh.faces()})
plotter.draw_edges()

plotter.show()