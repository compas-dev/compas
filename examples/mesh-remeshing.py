"""Remeshing a 2D mesh."""

from __future__ import print_function
from __future__ import division

import rhinoscriptsyntax as rs

import compas_rhino

from compas.datastructures import Mesh
from compas.datastructures import mesh_delaunay_from_points
from compas.datastructures import trimesh_remesh

from compas_rhino.conduits import MeshConduit


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


def callback(mesh, k, args):
    conduit = args[0]
    conduit.redraw(k)


boundary = rs.GetObject("Select Boundary Curve", 4)
length   = rs.GetReal("Select Edge Target Length", 2.0)
points   = rs.DivideCurve(boundary, rs.CurveLength(boundary) / length)

faces = mesh_delaunay_from_points(points, points)
mesh  = Mesh.from_vertices_and_faces(points, faces)

conduit = MeshConduit(mesh, refreshrate=2)

with conduit.enabled():
    trimesh_remesh(
        mesh,
        target=length,
        kmax=500,
        allow_boundary_split=True,
        allow_boundary_swap=True,
        callback=callback,
        callback_args=(conduit, )
    )

compas_rhino.mesh_draw(mesh, vertexcolor={key: '#ff0000' for key in mesh.vertices_on_boundary()})
