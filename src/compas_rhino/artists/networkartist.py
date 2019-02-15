from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas_rhino.artists import Artist

from compas_rhino.artists.mixins import VertexArtist
from compas_rhino.artists.mixins import EdgeArtist

try:
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['NetworkArtist']


class NetworkArtist(EdgeArtist, VertexArtist, Artist):
    """A network artist defines functionality for visualising COMPAS networks in Rhino.

    Parameters
    ----------
    network : compas.datastructures.Network
        A COMPAS network.
    layer : str, optional
        The name of the layer that will contain the network.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, network, layer=None):
        super(NetworkArtist, self).__init__(layer=layer)
        self.network = network
        self.defaults.update({
            'color.vertex' : (255, 255, 255),
            'color.edge'   : (0, 0, 0),
        })

    @property
    def network(self):
        """compas.datastructures.Network: The network that should be painted."""
        return self.datastructure

    @network.setter
    def network(self, network):
        self.datastructure = network

    def clear(self):
        """Clear the vertices and edges of the network, without clearing the
        other elements in the layer."""
        self.clear_vertices()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas_rhino.artists import NetworkArtist

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    artist = NetworkArtist(network, layer='NetworkArtist')

    artist.clear_layer()

    artist.draw_vertices()
    artist.redraw(0.0)

    artist.draw_vertexlabels()
    artist.redraw(1.0)

    artist.draw_edges()
    artist.redraw(1.0)

    artist.draw_edgelabels()
    artist.redraw(1.0)
