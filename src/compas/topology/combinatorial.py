from __future__ import print_function

from collections import deque
from compas.topology import bfs_traverse


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'vertex_coloring',
]


def vertex_coloring(adjacency):
    """Color the vertices of a network such that no two colors are adjacent.

    Parameters
    ----------
    network : compas.datastructures.Network
        The network object.

    Warning
    -------
    This is a greedy algorithm, so it might be slow for large networks.

    Example
    -------

    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter
        from compas.topology import vertex_coloring

        network = Network.from_obj(compas.get_data('grid_irregular.obj'))

        key_color = vertex_coloring(network.adjacency)
        colors = ['#ff0000', '#00ff00', '#0000ff']

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(facecolor={key: colors[key_color[key]] for key in network.vertices()})
        plotter.draw_edges()

        plotter.show()


    References
    ----------
    * http://scienceblogs.com/goodmath/2007/06/28/graph-coloring-algorithms-1/

    """
    key_to_color = {}
    key_to_degree = {key: len(adjacency[key]) for key in adjacency}
    vertices = sorted(adjacency.keys(), key=lambda key: key_to_degree[key])
    uncolored = deque(vertices[::-1])
    current_color = 0
    while uncolored:
        a = uncolored.popleft()
        key_to_color[a] = current_color
        colored_with_current = [a]
        for b in uncolored:
            if not any([b in adjacency[key] for key in colored_with_current]):
                key_to_color[b] = current_color
                colored_with_current.append(b)
        for key in colored_with_current[1:]:
            uncolored.remove(key)
        current_color += 1
    return key_to_color


def connected_components(adjacency):
    tovisit = set(adjacency)
    components = []
    while tovisit:
        root = tovisit.pop()
        visited = bfs_traverse(adjacency, root)
        tovisit -= visited
        components.append(list(visited))
    return components


def network_is_connected(network):
    """Verify that the mesh is connected.

    A mesh is connected if the following conditions are fulfilled:

    * For every two vertices a path exists connecting them.

    Returns
    -------
    bool
        True, if the mesh is connected.
        False, otherwise.

    """
    if not network.vertex:
        return False

    nodes = bfs_traverse(network.adjacency, network.get_any_vertex())

    return len(nodes) == network.number_of_vertices()


def mesh_is_connected(mesh):
    """Verify that the mesh is connected.

    A mesh is connected if the following conditions are fulfilled:

    * For every two vertices a path exists connecting them.

    Returns
    -------
    bool
        True, if the mesh is connected.
        False, otherwise.

    """
    if not mesh.vertex:
        return False

    nodes = bfs_traverse(mesh.adjacency, mesh.get_any_vertex())

    return len(nodes) == mesh.number_of_vertices()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    components = connected_components(network.adjacency)

    print(network_is_connected(network))
    print(components)

    key_color = vertex_coloring(network.adjacency)

    colors = ['#ff0000', '#00ff00', '#0000ff']

    plotter = NetworkPlotter(network, figsize=(10, 7))

    plotter.draw_vertices(facecolor={key: colors[key_color[key]] for key in network.vertices()})
    plotter.draw_edges()

    plotter.show()
