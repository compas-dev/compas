import compas

from compas.datastructures import Mesh
from compas.viewers import MeshViewer

from compas.numerical import fd_numpy

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

mesh.set_vertices_attribute('is_anchor', True, keys=mesh.vertices_where({'vertex_degree': 2}))
mesh.set_edges_attribute('q', 10.0, keys=mesh.edges_on_boundary())

# extract the structural data required for form finding
# run the force density method
# extract the updated coordinates from the result

key_index = mesh.key_index()

xyz   = mesh.get_vertices_attributes('xyz')
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
fixed = [key_index[key] for key in mesh.vertices_where({'is_anchor': True})]
edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]
q     = mesh.get_edges_attribute('q')

res = fd_numpy(xyz, edges, fixed, q, loads)
xyz = res[0]

# update the mesh coordinates
# and display the result

for index, (key, attr) in enumerate(mesh.vertices(True)):
    attr['x'] = xyz[index][0]
    attr['y'] = xyz[index][1]
    attr['z'] = xyz[index][2]

viewer = MeshViewer()
viewer.mesh = mesh

viewer.show()
