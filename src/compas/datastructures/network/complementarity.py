from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import combinations


__all__ = ["network_complement"]


def network_complement(network, cls=None):
    """Generate the complement network of a network.

    The complement of a graph G is the graph H with the same vertices
    but whose edges consists of the edges not present in the graph G [1]_.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A network.

    Returns
    -------
    :class:`~compas.datastructures.Network`
        The complement network.

    References
    ----------
    .. [1] Wolfram MathWorld. *Graph complement*.
           Available at: http://mathworld.wolfram.com/GraphComplement.html.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Network
    >>> from compas.datastructures import network_complement
    >>> network = Network.from_obj(compas.get('lines.obj'))
    >>> complement = network_complement(network)
    >>> any(complement.has_edge(u, v, directed=False) for u, v in network.edges())
    False

    """
    if not cls:
        cls = type(network)

    nodes = [network.node_coordinates(key) for key in network.nodes()]
    edges = [(u, v) for u, v in combinations(network.nodes(), 2) if not network.has_edge(u, v, directed=False)]

    return cls.from_nodes_and_edges(nodes, edges)
