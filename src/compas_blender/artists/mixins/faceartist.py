
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'FaceArtist',
]


class FaceArtist(object):

    __module__ = "compas_blender.artists.mixins"

    def clear_faces(self, keys=None):

        raise NotImplementedError


    def clear_facelabels(self, keys=None):

        raise NotImplementedError


    def draw_faces(self, keys=None, color=None, join_faces=False):

        raise NotImplementedError


    def draw_facelabels(self, text=None, color=None):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
