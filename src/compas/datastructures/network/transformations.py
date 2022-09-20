from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.geometry import transform_points


__all__ = [
    "network_transform",
    "network_transformed",
]


def network_transform(network, transformation):
    """Transform a network.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        The network.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation.

    Returns
    -------
    None

    Notes
    -----
    The network is modified in-place.

    """
    vertices = [network.node_coordinates(key) for key in network.nodes()]
    xyz = transform_points(vertices, transformation)
    for index, (key, attr) in enumerate(network.nodes(True)):
        attr["x"] = xyz[index][0]
        attr["y"] = xyz[index][1]
        attr["z"] = xyz[index][2]


def network_transformed(network, transformation):
    """Return a transformed copy of the network.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        The network.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation.

    Returns
    -------
    :class:`~compas.datastructures.Network`
        A transformed independent copy of `network`.

    Notes
    -----
    The original network is not modified.
    Instead a transformed independent copy is returned.

    """
    network_copy = network.copy()
    network_transform(network_copy, transformation)
    return network_copy
