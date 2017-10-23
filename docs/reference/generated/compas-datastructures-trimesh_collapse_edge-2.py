import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_split_face
from compas.datastructures import trimesh_swap_edge
from compas.datastructures import trimesh_collapse_edge
from compas.visualization import MeshPlotter

from compas.geometry import centroid_points

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

for fkey in list(mesh.faces()):
    vertices = mesh.face_vertices(fkey)
    mesh_split_face(mesh, fkey, vertices[0], vertices[2])

trimesh_swap_edge(mesh, 14, 16)
trimesh_swap_edge(mesh, 31, 22)

trimesh_collapse_edge(mesh, 30, 17)
trimesh_collapse_edge(mesh, 30, 31)
trimesh_collapse_edge(mesh, 30, 22)

points = mesh.get_vertices_attributes('xyz', keys=mesh.vertex_neighbours(30))
x, y, z = centroid_points(points)
attr = {'x': x, 'y': y, 'z': z}

mesh.set_vertex_attributes(30, attr)

plotter = MeshPlotter(mesh)

plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

plotter.show()