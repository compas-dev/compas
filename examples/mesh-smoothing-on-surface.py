"""Smoothing a mesh on a NURBS surface.

- make a mesh datastructure form a given Rhino mesh
- define a target surface
- smooth the mesh
- use a user-defined callback to pull the mesh back onto the surface at every iteration
- visualize with a conduit

"""

from __future__ import print_function

from compas.datastructures import Mesh
from compas.geometry import smooth_area

import compas_rhino

from compas_rhino.conduits import LinesConduit
from compas_rhino.geometry import RhinoSurface


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


def callback(vertices, k, args):
    conduit, edges, surf, fixed = args

    for key in vertices:
        if key not in fixed:
            x, y, z = surf.closest_point(vertices[key])
            vertices[key][0] = x
            vertices[key][1] = y
            vertices[key][2] = z

    conduit.lines = [[vertices[u], vertices[v]] for u, v in edges]
    conduit.redraw(k)


guid = compas_rhino.select_mesh()
mesh = compas_rhino.mesh_from_guid(Mesh, guid)

guid = compas_rhino.select_surface()
surf = RhinoSurface(guid)

fixed = set(mesh.vertices_on_boundary())

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
        callback_args=(conduit, edges, surf, fixed)
    )

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

compas_rhino.mesh_draw(mesh)
