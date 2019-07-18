from __future__ import print_function

import compas_rhino

from compas.datastructures import Mesh
from compas.geometry import smooth_area

from compas_rhino.conduits import LinesConduit

# define a callback for updating the conduit

def callback(k, args):
    conduit.lines = [[vertices[u], vertices[v]] for u, v in iter(edges)]
    conduit.redraw(k)


dz = 10

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

# add two additional fixed vertices
# on the inside of the mesh
# and set their z coordinates to a low point

for key in (161, 256):
    vertices[key][2] -= dz
    fixed.append(key)

# make a conduit for visualisation

edges = list(mesh.edges())
lines = [[vertices[u], vertices[v]] for u, v in edges]

conduit = LinesConduit(lines, refreshrate=5)

# run the smoothing algorithm
# update the mesh
# and display the results

with conduit.enabled():
    smooth_area(
        vertices,
        faces,
        adjacency,
        fixed=fixed,
        kmax=100,
        callback=callback)

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

compas_rhino.mesh_draw(mesh)
