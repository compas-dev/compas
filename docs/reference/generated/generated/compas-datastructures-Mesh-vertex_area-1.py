import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

k_a = {key: mesh.vertex_area(key) for key in mesh.vertices()}

plotter = MeshPlotter(mesh)
plotter.draw_vertices(
    radius=0.2,
    text={key: '{:.1f}'.format(k_a[key]) for key in mesh.vertices()}
)
plotter.draw_faces()
plotter.draw_edges()
plotter.show()