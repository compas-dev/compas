"""
Compute the equilibrium shape of an unloaded hypar using the force density method.

- make a mesh from a sample obj
- fix the corners and set the force densities
- run the fd method
- visualize the result

Note
----
This examples requires PyOpenGL for visualization.

"""

import compas

from compas.datastructures import Mesh
from compas.viewers import MeshViewer

from compas.numerical import fd_numpy


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


# make a mesh from an orthogonal grid of faces
# with two high corners and two low corners
# and define the default attributes of vertices and edges

mesh = Mesh.from_obj(compas.get('hypar.obj'))

dva = {'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0}
dea = {'q': 1.0}

mesh.update_default_vertex_attributes(dva)
mesh.update_default_edge_attributes(dea)


# mark the corners of the mesh as anchors
# i.e. they can take reaction forces
# increase the force density along the boundaries
# to prevent the mesh from collapsing too much

for key in mesh.vertices():
    mesh.vertex[key]['is_anchor'] = mesh.vertex_degree(key) == 2

for u, v in mesh.edges_on_boundary():
    mesh.edge[u][v]['q'] = 10.0


# extract the structural data required for form finding
# run the force density method
# extract the updated coordinates from the result

key_index = mesh.key_index()

xyz   = mesh.get_vertices_attributes('xyz')
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
fixed = [key_index[key] for key in mesh.vertices_where({'is_anchor': True})]
edges = mesh.indexed_edges()
q     = mesh.get_edges_attribute('q')

res = fd_numpy(xyz, edges, fixed, q, loads)
xyz = res[0]


# update the mesh coordinates
# and display the result

for index, (key, attr) in enumerate(mesh.vertices(True)):
    attr['x'] = xyz[index][0]
    attr['y'] = xyz[index][1]
    attr['z'] = xyz[index][2]

viewer = MeshViewer(mesh, 800, 600)
viewer.setup()
viewer.camera.zoom_in(5)
viewer.show()
