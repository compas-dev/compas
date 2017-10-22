import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

key = 17
nbrs = mesh.vertex_faces(key, ordered=True)

plotter = MeshPlotter(mesh)

plotter.draw_vertices(
    text={17: '17'},
    facecolor={17: '#ff0000'},
    radius=0.2
)
plotter.draw_faces(
    text={nbr: str(index) for index, nbr in enumerate(nbrs)},
    facecolor={nbr: '#cccccc' for nbr in nbrs}
)
plotter.draw_edges()
plotter.show()