from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures.network.core import BaseNetwork
from compas.datastructures.network.core import network_split_edge

from compas.datastructures.network.combinatorics import network_is_connected
from compas.datastructures.network.complementarity import network_complement
from compas.datastructures.network.transformations import network_transform
from compas.datastructures.network.transformations import network_transformed
from compas.datastructures.network.traversal import network_shortest_path
from compas.datastructures.network.smoothing import network_smooth_centroid


__all__ = ['Network']


class Network(BaseNetwork):

    complement = network_complement
    is_connected = network_is_connected
    shortest_path = network_shortest_path
    split_edge = network_split_edge
    smooth = network_smooth_centroid
    transform = network_transform
    transformed = network_transformed


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
