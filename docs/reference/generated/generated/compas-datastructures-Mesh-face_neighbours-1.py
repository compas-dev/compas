import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

key = 12
nbrs = mesh.face_neighbours(key)

text = {nbr: str(nbr) for nbr in nbrs}
text[key] = str(key)

color = {nbr: '#cccccc' for nbr in nbrs}
color[key] = '#ff0000'

plotter = MeshPlotter(mesh)
plotter.draw_vertices()
plotter.draw_faces(text=text, facecolor=color)
plotter.draw_edges()
plotter.show()