"""Mesh subdivision.

author : Tom Van Mele
email  : van.mele@arch.ethz.ch

"""

from __future__ import print_function
from __future__ import division

from compas.datastructures import Mesh
from compas.topology import mesh_subdivide

from compas_rhino.artists import MeshArtist
from compas_rhino.selectors import VertexSelector
from compas_rhino.modifiers import VertexModifier

# make a control mesh

mesh = Mesh.from_polyhedron(6)


# give it a name
# and set default vertex attributes

mesh.attributes['name'] = 'Control'
mesh.update_default_vertex_attributes({'is_fixed': False})


# make a drawing function for the control mesh

artist = MeshArtist(mesh, layer='SubdModeling::Control')

def draw():
    artist.clear_layer()
    artist.draw_vertices(color={key: '#ff0000' for key in mesh.vertices_where({'is_fixed': True})})
    artist.draw_edges()
    artist.redraw()


# draw the control mesh

draw()


# allow the user to change the attributes of the vertices
# note: the interaction loop exits
#       when the user cancels the selection of mesh vertices

while True:
    keys = VertexSelector.select_vertices(mesh)
    if not keys:
        break
    VertexModifier.update_vertex_attributes(mesh, keys)
    draw()


# make a subd mesh (using catmullclark)
# keep the vertices fixed
# as indicated by the user

fixed = mesh.vertices_where({'is_fixed': True})
subd = mesh_subdivide(mesh, scheme='catmullclark', k=5, fixed=fixed)


# give the mesh a (different) name

subd.attributes['name'] = 'Mesh'


# draw the result

artist.mesh = subd
artist.layer = 'SubdModeling::Mesh'

artist.clear_layer()
artist.draw()
