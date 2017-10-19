import compas

from compas.datastructures import Network
from compas.topology import dijkstra_distances
from compas.visualization import NetworkPlotter

network = Network.from_obj(compas.get_data('grid_irregular.obj'))

adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

target = 22

distances = dijkstra_distances(adjacency, weight, target)

plotter = NetworkPlotter(network)

plotter.draw_vertices(
    text={key: distances[key] for key in network.vertices()},
    facecolor='#eeeeee',
    radius=0.15
)
plotter.draw_edges()

plotter.show()