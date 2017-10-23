"""Smoothing a mesh.

"""

from compas.datastructures import Mesh
from compas.geometry import smooth_centroid
from compas.geometry import smooth_area

import compas_rhino as rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


guid = rhino.select_mesh()
mesh = rhino.mesh_from_guid(Mesh, guid)

vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
faces = {fkey: mesh.face_vertices(fkey) for fkey in mesh.faces()}
adjacency = {key: mesh.vertex_faces(key) for key in mesh.vertices()}

fixed = mesh.vertices_on_boundary()

smooth_area(vertices, faces, adjacency, fixed=fixed, kmax=100)

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

rhino.mesh_draw(mesh)
