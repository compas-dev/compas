"""Smoothing a mesh on a NURBS surface.

- make a mesh datastructure form a given Rhino mesh
- define a target surface
- smooth the mesh
- use a user-defined callback to pull the mesh back onto the surface at every iteration
- visualize with a conduit

"""

from __future__ import print_function

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import smooth_mesh_area
from compas.cad.rhino.conduits.mesh import MeshConduit
from compas.cad.rhino.geometry import RhinoSurface

import compas_rhino as rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


def callback(mesh, k, args):
    conduit, surf, fixed = args

    # pull the not fixed points back to the target surface
    surf.pull_mesh(mesh, fixed=fixed)

    # update the conduit
    conduit.redraw(k)


guid = rhino.select_mesh()
mesh = rhino.mesh_from_guid(Mesh, guid)

guid = rhino.select_surface()
surf = RhinoSurface(guid)

fixed = mesh.vertices_on_boundary()

conduit = MeshConduit(mesh, color=(255, 255, 255), refreshrate=2)

with conduit.enabled():
    smooth_mesh_area(mesh,
                     fixed,
                     kmax=100,
                     callback=callback,
                     callback_args=(conduit, surf, fixed))

rhino.draw_mesh(mesh)
