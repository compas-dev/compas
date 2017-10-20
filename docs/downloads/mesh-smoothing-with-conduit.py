"""Visualising mesh smoothing.

- smooth a given input mesh with constraints
- use a conduit for visualisation
- update the conduit using a user-defined callback function

"""

from __future__ import print_function

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import smooth_mesh_area

from compas.cad.rhino.conduits.mesh import MeshConduit

import compas_rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


def callback(mesh, k, args):
    conduit = args[0]
    conduit.redraw(k)


guid = compas_rhino.select_mesh()
mesh = compas_rhino.mesh_from_guid(Mesh, guid)

fixed = set(mesh.vertices_on_boundary())

for key in [161, 256]:
    mesh.vertex[key]['z'] -= 15
    fixed.add(key)

conduit = MeshConduit(mesh, refreshrate=5)

with conduit.enabled():
    smooth_mesh_area(mesh, fixed, kmax=100, callback=callback, callback_args=(conduit, ))

compas_rhino.draw_mesh(mesh)
