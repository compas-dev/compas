import compas
from compas.datastructures import FaceNetwork
from compas.visualization import FaceNetworkPlotter
from compas.datastructures import network_find_faces
from compas.datastructures import network_split_edge

network = FaceNetwork.from_obj(compas.get_data('lines.obj'))

network_find_faces(network, breakpoints=network.leaves())

a = network_split_edge(network, 0, 22)
b = network_split_edge(network, 2, 30)
c = network_split_edge(network, 17, 21)
d = network_split_edge(network, 28, 16)

lines = []
for u, v in network.edges():
    lines.append({
        'start': network.vertex_coordinates(u, 'xy'),
        'end'  : network.vertex_coordinates(v, 'xy'),
        'arrow': 'end',
        'width': 4.0,
        'color': '#00ff00'
    })

plotter = FaceNetworkPlotter(network)

plotter.draw_lines(lines)

plotter.draw_vertices(
    radius=0.2,
    text={key: key for key in network.vertices()},
    facecolor={key: '#ff0000' for key in (a, b, c, d)}
)
plotter.draw_edges()
plotter.draw_faces(
    text={fkey: fkey for fkey in network.faces()},
    facecolor={fkey: '#eeeeee' for fkey in network.faces()}
)

plotter.show()