"""Network 01: Shortest path

"""

import compas

from compas.datastructures.network import Network
from compas.datastructures.network.algorithms import network_dijkstra_path
from compas.visualization.plotters.networkplotter import NetworkPlotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


network = Network.from_obj(compas.get_data('grid_irregular.obj'))

# add weight to the edges
# corresponding to their length

weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

# choose start and end

start, end = 21, 22

# compute the shortest path

path = network_dijkstra_path(network.adjacency, weight, start, end)

# plot!

edges = []
for i in range(len(path) - 1):
    u = path[i]
    v = path[i + 1]
    if v not in network.edge[u]:
        u, v = v, u
    edges.append([u, v])

plotter = NetworkPlotter(network)

plotter.draw_vertices(
    text={key: key for key in (start, end)},
    facecolor={key: '#ff0000' for key in (path[0], path[-1])},
    radius=0.15
)

plotter.draw_edges(
    color={(u, v): '#ff0000' for u, v in edges},
    width={(u, v): 2.0 for u, v in edges},
    text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()}
)

plotter.show()
