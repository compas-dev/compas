"""Mesh 08: Subd modeling

The following code computes a solidified smooth mesh from a spatial network of lines.
The shown method yields similar results as the exoskeleton plugin for Grasshopper
to create meshes for 3D printing.

"""

from __future__ import print_function
from __future__ import division

import compas_rhino

from compas.datastructures import Mesh
from compas.geometry import Polyhedron
from compas.datastructures import mesh_subdivide


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# make a control mesh

cube = Polyhedron.generate(6)
mesh = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)

# give it a name
# and set default vertex attributes

mesh.attributes['name'] = 'Control'
mesh.update_default_vertex_attributes({'is_fixed': False})

# draw the control mesh
# with showing the faces

compas_rhino.mesh_draw(
    mesh,
    layer='SubdModeling::Control',
    clear_layer=True,
    show_faces=False,
    show_vertices=True,
    show_edges=True
)

# allow the user to change the attributes of the vertices
# note: the interaction loop exits
#       when the user cancels the selection of mesh vertices

while True:
    keys = compas_rhino.mesh_select_vertices(mesh)
    if not keys:
        break
    compas_rhino.mesh_update_vertex_attributes(mesh, keys)

# redraw the mesh to reflect the changes by the user

compas_rhino.mesh_draw(
    mesh,
    layer='SubdModeling::Control',
    clear_layer=True,
    show_faces=False,
    show_vertices=True,
    show_edges=True,
    vertexcolor={key: '#ff0000' for key in mesh.vertices_where({'is_fixed': True})}
)

# make a subd mesh (using catmullclark)
# keep the vertices fixed
# as indicated by the user

fixed = mesh.vertices_where({'is_fixed': True})
subd = mesh_subdivide(mesh, scheme='catmullclark', k=5, fixed=fixed)

# give the mesh a (different) name

subd.attributes['name'] = 'Mesh'

# draw the result

compas_rhino.mesh_draw(
    subd,
    layer='SubdModeling::Mesh',
    clear_layer=True,
    show_faces=True,
    show_vertices=False,
    show_edges=False
)
