import random

import compas
from compas.datastructures import Mesh
from compas.utilities import XFunc
from compas_rhino.artists import MeshArtist

dr = XFunc('compas.numerical.dr_numpy')

dva = {
    'is_fixed': False,
    'x': 0.0,
    'y': 0.0,
    'z': 0.0,
    'px': 0.0,
    'py': 0.0,
    'pz': 0.0,
    'rx': 0.0,
    'ry': 0.0,
    'rz': 0.0,
}

dea = {
    'qpre': 1.0,
    'fpre': 0.0,
    'lpre': 0.0,
    'linit': 0.0,
    'E': 0.0,
    'radius': 0.0,
}

mesh = Mesh.from_obj(compas.get('faces.obj'))

print('mesh')
print(mesh.number_of_vertices())

mesh.update_default_vertex_attributes(dva)
mesh.update_default_edge_attributes(dea)

for key, attr in mesh.vertices(True):
    attr['is_fixed'] = mesh.vertex_degree(key) == 2

for u, v, attr in mesh.edges(True):
    attr['qpre'] = 1.0 * random.randint(1, 7)

k_i = mesh.key_index()

vertices = mesh.get_vertices_attributes(('x', 'y', 'z'))
edges = [(k_i[u], k_i[v]) for u, v in mesh.edges()]
fixed = [k_i[key] for key in mesh.vertices_where({'is_fixed': True})]
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
qpre = mesh.get_edges_attribute('qpre')
fpre = mesh.get_edges_attribute('fpre')
lpre = mesh.get_edges_attribute('lpre')
linit = mesh.get_edges_attribute('linit')
E = mesh.get_edges_attribute('E')
radius = mesh.get_edges_attribute('radius')

xyz, q, f, l, r = dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius, kmax=100)

for key, attr in mesh.vertices(True):
    index = k_i[key]
    attr['x'] = xyz[index][0]
    attr['y'] = xyz[index][1]
    attr['z'] = xyz[index][2]

artist = MeshArtist(mesh, layer="XFunc::Mesh")

artist.clear_layer()

artist.draw_vertices()
artist.draw_edges()
artist.draw_faces()

artist.redraw()
