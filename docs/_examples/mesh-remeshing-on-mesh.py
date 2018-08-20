from __future__ import print_function

from compas.datastructures import Mesh
from compas.geometry import centroid_points
from compas.geometry import smooth_centroid
from compas.topology import trimesh_remesh
from compas.topology import mesh_quads_to_triangles

import compas_rhino

from compas_rhino.geometry import RhinoMesh
from compas_rhino.geometry import RhinoCurve
from compas_rhino.conduits import MeshConduit


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# set the remeshing parameters

length = 0.25
kmax = 300


# select the original mesh
# select the border
# select the fixed points

guid_target = compas_rhino.select_mesh()
guid_border = compas_rhino.select_polyline()
guid_points = compas_rhino.select_points()


# wrap the Rhino mesh object for convenience
# wrap the Rhino curve object for convenience
# get the point coordinates

target = RhinoMesh(guid_target)
border = RhinoCurve(guid_border)
points = compas_rhino.get_point_coordinates(guid_points)


# make a mesh datastructure from the Rhino mesh
# triangulate the mesh

mesh = compas_rhino.mesh_from_guid(Mesh, guid_target)
mesh_quads_to_triangles(mesh)


# identify the fixed vertices
# by matching the coordinates of the selected points
# up to a precision

keys  = compas_rhino.mesh_identify_vertices(mesh, points, '1f')
fixed = set(keys)


# create a conduit for visualisation
# define a callback
# for updating the conduit
# and for pulling the mesh back to the original during remeshing
# and for keeping the boundary on the boundary curve

conduit = MeshConduit(mesh, refreshrate=2)

def callback(mesh, k, args):
    boundary = set(mesh.vertices_on_boundary())
    for key, attr in mesh.vertices(data=True):
        if key in fixed:
            continue
        if key in boundary:
            x, y, z = border.closest_point(mesh.vertex_coordinates(key))
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z
        else:
            x, y, z = target.closest_point(mesh.vertex_coordinates(key))
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z
    conduit.redraw(k)


# run the remeshing algorithm
# draw the result

with conduit.enabled():
    trimesh_remesh(
        mesh,
        target=length,
        kmax=kmax,
        tol=0.1,
        divergence=0.01,
        allow_boundary_split=True,
        allow_boundary_swap=True,
        allow_boundary_collapse=False,
        smooth=True,
        fixed=fixed,
        callback=callback)


compas_rhino.mesh_draw(mesh, layer='remeshed', clear_layer=True)
