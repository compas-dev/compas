
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.artists import Artist
from compas_blender.artists.mixins import VertexArtist
from compas_blender.artists.mixins import EdgeArtist


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'NetworkArtist',
]


class NetworkArtist(EdgeArtist, VertexArtist, Artist):

    __module__ = "compas_blender.artists"

    def __init__(self, network, layer=None):
        super(NetworkArtist, self).__init__(layer=layer)

        self.network = network
        self.defaults.update({
            'color.vertex': (255, 255, 255),
            'color.edge':   (0, 0, 0),
        })


    @property
    def network(self):

        return self.datastructure


    @network.setter
    def network(self, network):

        self.datastructure = network


    def draw(self):

        raise NotImplementedError


    def clear(self):

        self.clear_vertices()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network


    network = Network.from_obj(compas.get('grid_irregular.obj'))

    artist = NetworkArtist(network=network)

    #artist.clear_layer()

    artist.draw_vertices(radius=0.05)
    artist.draw_vertexlabels()
    #artist.clear_vertexlabels()
    
    #artist.draw_edges()
    #artist.draw_edgelabels()
    #artist.clear_edgelabels()
