import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

key = 17
nbrs = mesh.vertex_neighbours(key, ordered=True)

plotter = MeshPlotter(mesh)

color = {nbr: '#cccccc' for nbr in nbrs}
color[key] = '#ff0000'

text = {nbr: str(index) for index, nbr in enumerate(nbrs)}
text[key] = str(key)

plotter.draw_vertices(text=text, facecolor=color)
plotter.draw_faces()
plotter.draw_edges()

plotter.show()