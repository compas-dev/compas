"""Smoothing a mesh.

"""

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import smooth_mesh_area

import compas_rhino as rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


guid = rhino.select_mesh()
mesh = rhino.mesh_from_guid(Mesh, guid)

fixed = mesh.vertices_on_boundary()

smooth_mesh_area(mesh, fixed, kmax=100)

rhino.draw_mesh(mesh)
