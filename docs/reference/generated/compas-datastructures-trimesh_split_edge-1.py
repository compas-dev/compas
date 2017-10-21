import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_split_face
from compas.datastructures import trimesh_split_edge

from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

for fkey in list(mesh.faces()):
    a, b, c, d = mesh.face_vertices(fkey)
    mesh_split_face(mesh, fkey, b, d)

split = trimesh_split_edge(mesh, 17, 30)

facecolor = {key: '#cccccc' if key != split else '#ff0000' for key in mesh.vertices()}

plotter = MeshPlotter(mesh)

plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2, facecolor=facecolor)
plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

plotter.show()