from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector


__all__ = [
    'network_select_vertices',
    'network_select_vertex',
    'network_select_edges',
    'network_select_edge'
]


# ==============================================================================
# selections
# ==============================================================================


def network_select_vertices(network, message="Select network vertices."):
    """Select vertices of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    message : str ("Select network vertices.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected vertices.

    Examples
    --------
    >>>

    See Also
    --------
    * :func:`network_select_vertex`

    """
    return VertexSelector.select_vertices(network)


def network_select_vertex(network, message="Select a network vertex"):
    """Select one vertex of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    message : str ("Select a network vertex.")
        The message to display to the user.

    Returns
    -------
    str
        The key of the selected vertex.
    None
        If no vertex was selected.

    See Also
    --------
    * :func:`network_select_vertices`

    """
    return VertexSelector.select_vertex(network)


def network_select_edges(network, message="Select network edges"):
    """Select edges of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        The network object.
    message : str ("Select network edges.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected edges. Each key is a *uv* pair.

    See Also
    --------
    * :func:`network_select_edge`

    """
    return EdgeSelector.select_edges(network)


def network_select_edge(network, message="Select a network edge"):
    """Select one edge of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    message : str ("Select a network edge.")
        The message to display to the user.

    Returns
    -------
    tuple
        The key of the selected edge.
    None
        If no edge was selected.

    See Also
    --------
    * :func:`network_select_edges`

    """
    return EdgeSelector.select_edge(network)
