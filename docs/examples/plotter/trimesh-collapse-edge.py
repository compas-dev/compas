import compas

from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

plotter.show()
# import compas

# from compas.datastructures import Mesh
# from compas.datastructures import mesh_quads_to_triangles
# from compas.datastructures import trimesh_collapse_edge
# from compas_plotters import MeshPlotter

# mesh = Mesh.from_obj(compas.get('faces.obj'))

# mesh_quads_to_triangles(mesh)

# u, v = mesh.get_any_edge()

# trimesh_collapse_edge(mesh, u, v)

# plotter = MeshPlotter(mesh)

# plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
# plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

# plotter.show()
