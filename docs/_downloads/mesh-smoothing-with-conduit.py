"""Visualising mesh smoothing.

- smooth a given input mesh with constraints
- use a conduit for visualisation
- update the conduit using a user-defined callback function

"""

from __future__ import print_function

from compas.datastructures import Mesh
from compas.geometry import smooth_area

from compas_rhino.conduits import LinesConduit

import compas_rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


def callback(vertices, k, args):
    conduit, edges = args
    conduit.lines = [[vertices[u], vertices[v]] for u, v in iter(edges)]
    conduit.redraw(k)


guid = compas_rhino.select_mesh()
mesh = compas_rhino.mesh_from_guid(Mesh, guid)

fixed = set(mesh.vertices_on_boundary())

for key in [161, 256]:
    mesh.vertex[key]['z'] -= 15
    fixed.add(key)

vertices  = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
faces     = {key: mesh.face_vertices(key) for key in mesh.faces()}
adjacency = {key: mesh.vertex_faces(key) for key in mesh.vertices()}

edges = list(mesh.edges())
lines = [[vertices[u], vertices[v]] for u, v in edges]

conduit = LinesConduit(lines, refreshrate=5)

with conduit.enabled():
    smooth_area(
        vertices,
        faces,
        adjacency,
        fixed=fixed,
        kmax=100,
        callback=callback,
        callback_args=(conduit, edges)
    )

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

compas_rhino.mesh_draw(mesh)
