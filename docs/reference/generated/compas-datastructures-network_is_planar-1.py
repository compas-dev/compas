import compas

from compas.datastructures import Network
from compas.datastructures import network_is_planar
from compas.datastructures import network_find_crossings
from compas.visualization import NetworkPlotter

network = Network.from_obj(compas.get_data('lines.obj'))

network.add_edge(21, 29)
network.add_edge(17, 28)

if not network_is_planar(network):
    crossings = network_find_crossings(network)
else:
    crossings = []

plotter = NetworkPlotter(network)

plotter.draw_vertices(radius=0.15, text={key: key for key in network.vertices()})
plotter.draw_edges(color={edge: '#ff0000' for edges in crossings for edge in edges})

plotter.show()