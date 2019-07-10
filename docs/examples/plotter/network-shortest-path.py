"""Shortest path in a network

author : Tom Van Mele
email  : van.mele@arch.ethz.ch

"""

from random import choice

import compas

from compas.utilities import pairwise
from compas.datastructures import Network
from compas.topology import dijkstra_path
from compas_plotters import NetworkPlotter


# make a network from a sample file

network = Network.from_obj(compas.get('grid_irregular.obj'))


# start and end

leaves = list(network.vertices_where({'vertex_degree': 1}))

start = end = 0
while start == end:
    start = choice(leaves)
    end = choice(leaves)

# construc an adjacency dict
# add weight to the edges corresponding to their length
# compute the shortest path

adjacency = {key: network.vertex_neighbors(key) for key in network.vertices()}

weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

path = dijkstra_path(adjacency, weight, start, end)


# visualize the result

plotter = NetworkPlotter(network, figsize=(10, 8), fontsize=6)

edges = []
for u, v in pairwise(path):
    if v not in network.edge[u]:
        u, v = v, u
    edges.append([u, v])

plotter.draw_vertices(
    text={key: key for key in (start, end)},
    facecolor={key: '#ff0000' for key in (path[0], path[-1])},
    radius=0.15
)

plotter.draw_edges(
    color={(u, v): '#ff0000' for u, v in edges},
    width={(u, v): 3.0 for u, v in edges},
    text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()}
)

plotter.show()
