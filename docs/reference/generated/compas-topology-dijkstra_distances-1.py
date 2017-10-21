import compas

from compas.datastructures import Network
from compas.topology import dijkstra_distances
from compas.visualization import NetworkPlotter
from compas.utilities import i_to_red

network = Network.from_obj(compas.get_data('grid_irregular.obj'))

adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

target = 22

distances = dijkstra_distances(adjacency, weight, target)

plotter = NetworkPlotter(network)

dmax = max(distances.values())

facecolor = {key: i_to_red(distances[key] / dmax) for key in network.vertices()}
text = {key: '{:.1f}'.format(distances[key]) for key in network.vertices()}

plotter.draw_vertices(
    text=text,
    facecolor=facecolor,
    radius=0.15
)
plotter.draw_edges()

plotter.show()