from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.modifiers import Modifier
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier


__all__ = [
    'network_update_attributes',
    'network_update_vertex_attributes',
    'network_update_edge_attributes',

    'network_move',
    'network_move_vertex',
]


# ==============================================================================
# modifications
# ==============================================================================


def network_move(network):
    """Move the entire network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.

    See Also
    --------
    * :func:`network_move_vertex`

    """
    return Modifier.move(network)


def network_update_attributes(network):
    """Update the attributes of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`network_update_vertex_attributes`
    * :func:`network_update_edge_attributes`

    """
    return Modifier.update_attributes(network)


def network_move_vertex(network, key, constraint=None, allow_off=False):
    """Move on vertex of the network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    key : str
        The vertex to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    return VertexModifier.move_vertex(network, key, constraint=constraint, allow_off=allow_off)


def network_update_vertex_attributes(network, keys, names=None):
    """Update the attributes of the vertices of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    keys : tuple, list
        The keys of the vertices to update.
    names : tuple, list (None)
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`network_update_attributes`
    * :func:`network_update_edge_attributes`

    """
    return VertexModifier.update_vertex_attributes(network, keys, names=names)


def network_update_edge_attributes(network, keys, names=None):
    """Update the attributes of the edges of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    keys : tuple, list
        The keys of the edges to update.
    names : tuple, list (None)
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`network_update_attributes`
    * :func:`network_update_vertex_attributes`

    """
    return EdgeModifier.update_edge_attributes(network, keys, names=names)
