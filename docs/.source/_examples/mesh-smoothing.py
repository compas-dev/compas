"""Smoothing a mesh.

"""

from compas.datastructures import Mesh
from compas.geometry import smooth_area

import compas_rhino as rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


guid = rhino.select_mesh()
mesh = rhino.mesh_from_guid(Mesh, guid)

vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
adjacency = {key: mesh.vertex_neighbours(key) for key in mesh.vertices()}
fixed = mesh.vertices_on_boundary()

smooth_area(vertices, adjacency, fixed=fixed, kmax=100)

rhino.mesh_draw(mesh)
