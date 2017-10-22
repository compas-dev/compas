import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

key, fkeys = mesh.insert_vertex(12, return_fkeys=True)

plotter = MeshPlotter(mesh)
plotter.draw_vertices(radius=0.15, text={key: str(key)})
plotter.draw_faces(text={fkey: fkey for fkey in fkeys})
plotter.show()