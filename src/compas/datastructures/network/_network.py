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
    from compas.datastructures import Mesh
    from compas.datastructures import network_find_cycles
    from compas_plotters import NetworkPlotter
    from compas_plotters import MeshPlotter

    # nodes = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0]]
    # edges = [[0, 1], [1, 2], [3, 4], [4, 5], [0, 3], [1, 4], [2, 5], [0, 4], [1, 5], [1, 3], [2, 4]]

    data = {0: [-40.0, 55.0, 0.0], 1: [-35.0, 55.0, 0.0], 2: [-30.0, 55.0, 0.0], 4: [-35.0, 60.0, 0.0], 6: [-37.5, 57.5, 0.0], 7: [-32.5, 57.5, 0.0], 8: [-40.0, 53.82, 0.0], 10: [-30.0, 53.82, 0.0], 11: [-35.0, 61.18, 0.0]}
    # key_index = {key: index for index, key in enumerate(data)}

    # nodes = data.values()
    edges = [(0, 8), (0, 1), (1, 2), (10, 2), (0, 6), (6, 4), (4, 11), (4, 7), (7, 2)]
    # edges = [(key_index[u], key_index[v]) for u, v in edges]

    # net = Network.from_nodes_and_edges(nodes, edges)
    # network = net.copy()

    network = Network()

    for key, xyz in data.items():
        network.add_node(key, x=xyz[0], y=xyz[1], z=xyz[2])
    for u, v in edges:
        network.add_edge(u, v)

    points = {key: network.node_coordinates(key) for key in network.nodes()}
    cycles = network_find_cycles(network, breakpoints=network.leaves())

    mesh = Mesh.from_vertices_and_faces(points, cycles)

    # e1 = network.edge_coordinates(0, 4)
    # e2 = network.edge_coordinates(1, 3)

    # xyz = intersection_line_line_xy(e1, e2)

    # network.delete_edge(0, 4)
    # network.delete_edge(1, 3)

    # x = network.add_node(x=xyz[0], y=xyz[1], z=xyz[2])

    # network.add_edge(x, 0)
    # network.add_edge(x, 1)
    # network.add_edge(x, 3)
    # network.add_edge(x, 4)

    # plotter = NetworkPlotter(network, figsize=(8, 5))
    # plotter.draw_nodes(text='key', radius=0.25)
    # plotter.draw_edges()
    # plotter.show()

    plotter = MeshPlotter(mesh, figsize=(8, 5))
    plotter.draw_vertices(text='key', radius=0.25)
    plotter.draw_edges(keys=list(set(mesh.edges()) - set(mesh.edges_on_boundary())))
    plotter.draw_faces(text='key', keys=list(set(mesh.faces()) - set(mesh.faces_on_boundary())))
    plotter.save('find_cycles.png')
