import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_smooth_centroid
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

mesh_smooth_centroid(mesh, fixed=fixed, kmax=10)

plotter = MeshPlotter(mesh)

plotter.draw_vertices()
plotter.draw_edges()

plotter.show()