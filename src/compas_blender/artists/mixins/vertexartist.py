
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'VertexArtist',
]


class VertexArtist(object):

    __module__ = "compas_blender.artists.mixins"

    def clear_vertices(self, keys=None):

        raise NotImplementedError


    def clear_vertexlabels(self, keys=None):

        raise NotImplementedError


    def draw_vertices(self, keys=None, color=None):

        raise NotImplementedError


    def draw_vertexlabels(self, text=None, color=None):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
