from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures.network.core import BaseNetwork
from compas.datastructures.network.core import network_split_edge


__all__ = ['Network']


class Network(BaseNetwork):

    __module__ = "compas.datastructures"

    split_edge = network_split_edge


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    from compas.geometry import intersection_line_line_xy
    from compas_plotters import NetworkPlotter

    nodes = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0]]
    edges = [[0, 1], [1, 2], [3, 4], [4, 5], [0, 3], [1, 4], [2, 5], [0, 4], [1, 5], [1, 3], [2, 4]]
    net = Network.from_nodes_and_edges(nodes, edges)

    network = net.copy()

    e1 = network.edge_coordinates(0, 4)
    e2 = network.edge_coordinates(1, 3)

    xyz = intersection_line_line_xy(e1, e2)

    network.delete_edge(0, 4)
    network.delete_edge(1, 3)

    x = network.add_node(x=xyz[0], y=xyz[1], z=xyz[2])

    network.add_edge(x, 0)
    network.add_edge(x, 1)
    network.add_edge(x, 3)
    network.add_edge(x, 4)

    plotter = NetworkPlotter(network, figsize=(8, 5))
    plotter.draw_nodes(text='key', radius=0.03)
    plotter.draw_edges()
    plotter.show()
