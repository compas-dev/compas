import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

root = 17
nbrs = mesh.vertex_neighbours(root, ordered=True)

text = {nbr: str(i) for i, nbr in enumerate(nbrs)}
text[root] = root

fcolor = {nbr: '#cccccc' for nbr in nbrs}
fcolor[root] = '#ff0000'

plotter.draw_vertices(
    text=text,
    facecolor=fcolor
)
plotter.draw_faces()
plotter.draw_edges()

plotter.show()