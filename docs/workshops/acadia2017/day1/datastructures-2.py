import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

key  = 17
nbrs = mesh.vertex_neighbours(key, ordered=True)

text   = {nbr: str(index) for index, nbr in enumerate(nbrs)}
fcolor = {key: '#cccccc' for key in nbrs}

fcolor[17] = '#ff0000'

plotter.draw_vertices(text=text, facecolor=fcolor)
plotter.draw_faces()
plotter.draw_edges()

plotter.show()