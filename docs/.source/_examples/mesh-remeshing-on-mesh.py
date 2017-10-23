from __future__ import print_function

from compas.utilities import geometric_key
from compas.geometry import centroid_points
from compas.datastructures import Mesh
from compas.datastructures import trimesh_remesh
from compas.geometry import smooth_centroid
from compas.datastructures import mesh_quads_to_triangles

import compas_rhino

from compas_rhino.geometry import RhinoMesh
from compas_rhino.geometry import RhinoCurve
from compas_rhino.conduits import MeshConduit


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


def callback(mesh, k, args):
    conduit, fixed, target, border = args

    # prevent the dreaded Rhino spinning wheel
    compas_rhino.wait()

    boundary = set(mesh.vertices_on_boundary())

    # pull the mesh vertices back to the target and border
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

    # update the conduit at the specified rate
    conduit.redraw(k)


# get the target mesh
# and its border

guid_target = compas_rhino.select_mesh()
guid_border = compas_rhino.select_polyline()

# get fixed points

points = compas_rhino.get_point_coordinates(compas_rhino.select_points())

# make a remeshing mesh

mesh = compas_rhino.mesh_from_guid(Mesh, guid_target)

mesh_quads_to_triangles(mesh)

# update its attributes

mesh.update_default_vertex_attributes({'is_fixed': False})

# make the target and border objects

target = RhinoMesh(guid_target)
border = RhinoCurve(guid_border)

# make a map of vertex coorindates
# with 1 float precision

gkey_key = {geometric_key(mesh.vertex_coordinates(key), '1f'): key for key in mesh.vertices()}

# identify fixed points

for xyz in points:
    gkey = geometric_key(xyz, '1f')
    if gkey in gkey_key:
        key = gkey_key[gkey]
        mesh.vertex[key]['is_fixed'] = True

# find the fixed vertices

fixed = set(mesh.vertices_where({'is_fixed': True}))

# create a conduit for visualisation

conduit = MeshConduit(mesh, color=(255, 255, 255), refreshrate=5)

# set the target length

target_length = 0.25

# visualise the process with a conduit
with conduit.enabled():
    trimesh_remesh(
        mesh,
        target_length,
        tol=0.1,
        divergence=0.01,
        kmax=500,
        allow_boundary_split=True,
        allow_boundary_collapse=True,
        smooth=True,
        fixed=fixed,
        callback=callback,
        callback_args=(conduit, fixed, target, border)
    )

compas_rhino.mesh_draw(mesh, layer='remeshed', clear_layer=True)
