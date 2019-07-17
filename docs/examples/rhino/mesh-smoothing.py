from compas.datastructures import Mesh
from compas.geometry import smooth_area

import compas_rhino

# select a Rhino mesh
# and make it into a mesh datastructure

guid = compas_rhino.select_mesh()
mesh = compas_rhino.mesh_from_guid(Mesh, guid)

# extract the data needed by the smoothing algorithm
# identify the boundary as fixed

vertices  = mesh.get_vertices_attributes('xyz')
faces     = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
adjacency = [mesh.vertex_faces(key, ordered=True) for key in mesh.vertices()]
fixed     = mesh.vertices_on_boundary()

# run the smoothing algorithm
# update the mesh
# display the result in Rhino

smooth_area(vertices, faces, adjacency, fixed=fixed, kmax=100)

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

compas_rhino.mesh_draw(mesh)
