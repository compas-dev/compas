""""""

import compas

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.viewer import MeshViewer

from compas.numerical.methods.forcedensity import fd


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


# make a mesh from an orthogonal grid of faces
# with two high corners
# and two low corners

mesh = Mesh.from_obj(compas.get_data('hypar.obj'))

# define the default attributes of vertices and edges

dva = {'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': -0.0}
dea = {'q': 1.0}

# update the default attributes of vertices and edges

mesh.update_default_vertex_attributes(dva)
mesh.update_default_edge_attributes(dea)

# mark the corners of the mesh as anchors
# i.e. they can take reaction forces

for key in mesh.vertices():
    mesh.vertex[key]['is_anchor'] = mesh.vertex_degree(key) == 2

# increase the force density along the boundaries
# to prevent the mesh from collapsing too much

for u, v in mesh.edges_on_boundary():
    mesh.edge[u][v]['q'] = 10.0

# extract the structural data required for form finding

xyz = mesh.get_vertices_attributes('xyz')
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
fixed = mesh.vertices_where({'is_anchor': True})
edges = mesh.indexed_edges()
q = mesh.get_edges_attribute('q')

# run the force density method
# extract the updated coordinates from the result

res = fd(xyz, edges, fixed, q, loads)
xyz = res[0]

# update the mesh coordinates

for index, (key, attr) in enumerate(mesh.vertices(True)):
    attr['x'] = xyz[index][0]
    attr['y'] = xyz[index][1]
    attr['z'] = xyz[index][2]

# display the result

viewer = MeshViewer(mesh, 800, 600)
viewer.setup()
viewer.show()
