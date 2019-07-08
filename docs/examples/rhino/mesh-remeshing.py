"""Remeshing a 2D mesh."""

from __future__ import print_function
from __future__ import division

import rhinoscriptsyntax as rs

import compas_rhino

from compas.datastructures import Mesh
from compas.topology import delaunay_from_points
from compas.topology import trimesh_remesh

from compas_rhino.conduits import MeshConduit


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# get the boundary curve
# and divide into segments of a specific length

boundary = rs.GetObject("Select Boundary Curve", 4)
length   = rs.GetReal("Select Edge Target Length", 2.0)
points   = rs.DivideCurve(boundary, rs.CurveLength(boundary) / length)


# generate a delaunay triangulation
# from the points on the boundary

faces = delaunay_from_points(points, boundary=points)
mesh = Mesh.from_vertices_and_faces(points, faces)


# make a conduit for visualization
# and a callback for updating the conduit

conduit = MeshConduit(mesh, refreshrate=2)

def callback(mesh, k, args):
    conduit.redraw(k)


# run the remeshing algorithm
# and draw the result

with conduit.enabled():
    trimesh_remesh(
        mesh,
        target=length,
        kmax=500,
        allow_boundary_split=True,
        allow_boundary_swap=True,
        callback=callback)

compas_rhino.mesh_draw(
    mesh,
    vertexcolor={key: '#ff0000' for key in mesh.vertices_on_boundary()})
