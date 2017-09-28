"""Remeshing a 2D mesh."""

from __future__ import print_function

import rhinoscriptsyntax as rs

import compas_rhino

from compas.datastructures.mesh import Mesh

from compas.datastructures.mesh.algorithms import delaunay_from_points
from compas.datastructures.mesh.algorithms import optimise_trimesh_topology

from compas.cad.rhino.conduits.mesh import MeshConduit


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


def callback(mesh, k, args):
    conduit = args[0]
    conduit.redraw(k)


boundary = rs.GetObject("Select Boundary Curve", 4)
target_length = rs.GetReal("Select Edge Target Length", 2.5)
points = rs.DivideCurve(boundary, rs.CurveLength(boundary) / target_length)

faces = delaunay_from_points(points, points)

mesh = Mesh.from_vertices_and_faces(points, faces)

conduit = MeshConduit(mesh, refreshrate=2)

with conduit.enabled():
    optimise_trimesh_topology(mesh,
                              target_length,
                              kmax=250,
                              callback=callback,
                              callback_args=(conduit, ))

compas_rhino.draw_mesh(mesh)
