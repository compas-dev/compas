from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas_ghpython.artists.mixins import VertexArtist
from compas_ghpython.artists.mixins import EdgeArtist


__all__ = ['NetworkArtist']


class NetworkArtist(EdgeArtist, VertexArtist):
    """A network artist defines functionality for visualising COMPAS networks in GhPython.

    Parameters
    ----------
    network : compas.datastructures.Network
        A COMPAS network.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, network):
        self.network = network
        self.defaults = {
            'color.vertex' : (255, 255, 255),
            'color.edge'   : (0, 0, 0),
        }

    @property
    def network(self):
        """compas.datastructures.Network: The network that should be painted."""
        return self.datastructure

    @network.setter
    def network(self, network):
        self.datastructure = network

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas_ghpython.artists.networkartist import NetworkArtist

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    artist = NetworkArtist(network)

    vertices = artist.draw_vertices()
    edges = artist.draw_edges()

