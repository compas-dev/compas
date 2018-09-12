from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time

import compas
import compas_rhino

from compas.utilities import color_to_colordict

from compas_rhino.artists.mixins import VertexArtist
from compas_rhino.artists.mixins import EdgeArtist

try:
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['NetworkArtist']


class NetworkArtist(EdgeArtist, VertexArtist):
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

    def __init__(self, network, layer=None):
        self.network = network
        self.layer = layer
        self.defaults = {
            'color.vertex': (0, 0, 0),
            'color.edge'  : (0, 0, 0),
        }

    @property
    def layer(self):
        """str: The layer that contains the network."""
        return self.datastructure.attributes.get('layer')

    @layer.setter
    def layer(self, value):
        self.datastructure.attributes['layer'] = value

    @property
    def network(self):
        """compas.datastructures.Network: The network that should be painted."""
        return self.datastructure

    @network.setter
    def network(self, network):
        self.datastructure = network

    def redraw(self, timeout=None):
        """Redraw the Rhino view.

        Parameters
        ----------
        timeout : float, optional
            The amount of time the artist waits before updating the Rhino view.
            The time should be specified in seconds.
            Default is ``None``.

        """
        if timeout:
            time.sleep(timeout)
        rs.EnableRedraw(True)
        rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()

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
    from compas_rhino.artists.networkartist import NetworkArtist

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
