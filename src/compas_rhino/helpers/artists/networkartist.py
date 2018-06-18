import time

from compas.utilities import color_to_colordict

import compas_rhino

from compas_rhino.helpers.artists.mixins import VertexArtist
from compas_rhino.helpers.artists.mixins import EdgeArtist
# from compas_rhino.helpers.artists.mixins import PathArtist
# from compas_rhino.helpers.artists.mixins import ForceArtist

try:
    import rhinoscriptsyntax as rs

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['NetworkArtist']


class NetworkArtist(EdgeArtist, VertexArtist):
    """"""

    def __init__(self, network, layer=None):
        self.datastructure = network
        self.layer = layer
        self.defaults = {
            'color.vertex': (0, 0, 0),
            'color.edge'  : (0, 0, 0),
        }

    # this should be called 'update_view'
    # 'redraw' should draw the network again, with the same settings
    def redraw(self, timeout=None):
        """Redraw the Rhino view."""
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
        self.clear_vertices()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas_rhino.helpers.artists.networkartist import NetworkArtist

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
