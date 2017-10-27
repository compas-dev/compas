import compas

from compas.datastructures import Mesh
from compas.visualization import MeshPlotter
from compas.numerical import fd
from compas.utilities import i_to_black

# make a mesh
# add default attributes for form finding

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.update_default_vertex_attributes({'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
mesh.update_default_edge_attributes({'q': 1.0})

# identify the anchors
# move two anchors up to create anticlastic boundary conditions

for key, attr in mesh.vertices(True):
    attr['is_anchor'] = mesh.vertex_degree(key) == 2
    if key in (18, 35):
        attr['z'] = 5.0

# preprocess

k_i   = mesh.key_index()
xyz   = mesh.get_vertices_attributes(('x', 'y', 'z'))
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
q     = mesh.get_edges_attribute('q')
fixed = mesh.vertices_where({'is_anchor': True})
fixed = [k_i[k] for k in fixed]
edges = [(k_i[u], k_i[v]) for u, v in mesh.edges()]

# compute equilibrium
# update the mesh geometry

xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads, rtype='list')

for key, attr in mesh.vertices(True):
    index = k_i[key]
    attr['x'] = xyz[index][0]
    attr['y'] = xyz[index][1]
    attr['z'] = xyz[index][2]

# visualisae the result
# color the vertices according to their elevation

plotter = MeshPlotter(mesh)

zmax = max(mesh.get_vertices_attribute('z'))

plotter.draw_vertices(
    facecolor={key: i_to_black(attr['z'] / zmax) for key, attr in mesh.vertices(True)}
)
plotter.draw_faces()
plotter.draw_edges()
plotter.show()