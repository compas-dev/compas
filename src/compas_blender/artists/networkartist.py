
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

        pass


    @property
    def network(self):

        raise NotImplementedError


    @network.setter
    def network(self, network):

        raise NotImplementedError


    def draw(self):

        raise NotImplementedError


    def clear(self):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
