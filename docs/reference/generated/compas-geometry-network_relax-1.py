import compas
from compas.datastructures import Network
from compas.visualization import NetworkPlotter
from compas.geometry import network_relax

network = Network.from_obj(compas.get('lines.obj'))

dva = {'is_fixed': False, 'p': [0.0, 0.0, 0.0], 'v': [0.0, 0.0, 0.0]}
dea = {'q': 1.0}

network.update_default_vertex_attributes(dva)
network.update_default_edge_attributes(dea)

for key, attr in network.vertices(True):
    attr['is_fixed'] = network.is_vertex_leaf(key)

for index, (u, v, attr) in enumerate(network.edges(True)):
    if index % 2 == 0:
        attr['q'] = 5.0

lines = []
for u, v in network.edges():
    lines.append({
        'start' : network.vertex_coordinates(u, 'xy'),
        'end'   : network.vertex_coordinates(v, 'xy'),
        'color' : '#cccccc',
        'width' : 1.0
    })

network_relax(network, kmax=100)

plotter = NetworkPlotter(network)

plotter.draw_lines(lines)
plotter.draw_vertices(
    facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})}
)
plotter.draw_edges()

plotter.show()