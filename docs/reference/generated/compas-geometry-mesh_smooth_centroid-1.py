import compas

from compas.datastructures import Mesh
from compas.visualization import MeshPlotter
from compas.geometry import mesh_smooth_centroid

mesh = Mesh.from_obj(compas.get('faces.obj'))
fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

mesh_smooth_centroid(mesh, fixed=fixed)

plotter = MeshPlotter(mesh)

plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
plotter.draw_faces()
plotter.draw_edges()

plotter.show()