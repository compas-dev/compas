import compas_rhino

from compas.cad.rhino.conduits import MeshConduit
from compas.cad.rhino.geometry import RhinoSurface

from compas.utilities import i_to_rgb

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import planarize_mesh
from compas.datastructures.mesh.algorithms import planarize_mesh_shapeop
from compas.datastructures.mesh.algorithms import flatness


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


# define a callback to visualise the planarisation process

def callback(mesh, k, args):
    conduit, surf, fixed = args

    for key, attr in mesh.vertices(True):
        if key in fixed:
            attr['z'] = 0

    # surf.pull_mesh(mesh, fixed=fixed, d=0.1)

    conduit.redraw(k)


# select an input surface and convert it to a mesh

guid = compas_rhino.select_surface('Select an input surface.')
mesh = compas_rhino.mesh_from_surface_heightfield(Mesh, guid, density=(20, 10))

fixed = mesh.vertices_where({'z': (-0.5, 0.1)})

# create a surface constraint

surf = RhinoSurface(guid)

# make a copy for planarisation

flat = mesh.copy()

mesh.attributes['name'] = 'Mesh'
flat.attributes['name'] = 'FlatMesh'

# draw the original mesh

dev0 = flatness(mesh)
dmax = max(dev0.values())

compas_rhino.helpers.mesh.draw_mesh_as_faces(
    mesh,
    layer='mesh_start',
    clear_layer=True,
    facecolor={fkey: i_to_rgb(dev0[fkey] / dmax) for fkey in mesh.faces()}
)

# make a conduit for visualisation of the planarisation process

conduit = MeshConduit(flat, color=(255, 255, 255), refreshrate=5)

# run the planarisation algorithm with the conduit enabled

with conduit.enabled():
    planarize_mesh(flat, kmax=500, callback=callback, callback_args=(conduit, surf, fixed))

# planarize_mesh_shapeop(flat, kmax=500, fixed=fixed)

# compute the *flatness*
# and draw the result

dev1 = flatness(flat)

compas_rhino.helpers.mesh.draw_mesh_as_faces(
    flat,
    layer='mesh_end',
    clear_layer=True,
    facecolor={fkey: i_to_rgb(dev1[fkey] / dmax) for fkey in flat.faces()}
)
