import compas
from compas.datastructures import Network
from compas.visualization import NetworkPlotter
from compas.numerical import dr

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

network = Network.from_obj(compas.get('lines.obj'))
network.update_default_vertex_attributes(dva)
network.update_default_edge_attributes(dea)

for key, attr in network.vertices(True):
    attr['is_fixed'] = network.vertex_degree(key) == 1

count = 1
for u, v, attr in network.edges(True):
    attr['qpre'] = count
    count += 1

k2i = dict((key, index) for index, key in enumerate(network.vertices()))

vertices = [network.vertex_coordinates(key) for key in network.vertex]
edges    = [(k2i[u], k2i[v]) for u, v in network.edges()]
fixed    = [k2i[key] for key, attr in network.vertices(True) if attr['is_fixed']]
loads    = [(attr['px'], attr['py'], attr['pz']) for key, attr in network.vertices(True)]
qpre     = [attr['qpre'] for u, v, attr in network.edges(True)]
fpre     = [attr['fpre'] for u, v, attr in network.edges(True)]
lpre     = [attr['lpre'] for u, v, attr in network.edges(True)]
linit    = [attr['linit'] for u, v, attr in network.edges(True)]
E        = [attr['E'] for u, v, attr in network.edges(True)]
radius   = [attr['radius'] for u, v, attr in network.edges(True)]

plotter = NetworkPlotter(network)

lines = []
for u, v in network.edges():
    lines.append({
        'start': network.vertex_coordinates(u, 'xy'),
        'end'  : network.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0
    })

xyz, q, f, l, r = dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius)

plotter.draw_lines(lines)
plotter.draw_vertices(
    facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})})
plotter.draw_edges()
plotter.show()