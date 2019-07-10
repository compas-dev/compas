import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_face_matrix

mesh = Mesh.from_obj(compas.get('faces.obj'))

F   = mesh_face_matrix(mesh)
xyz = array([mesh.vertex_coordinates(key) for key in mesh.vertices()])
c   = F.dot(xyz) / normrow(F)

