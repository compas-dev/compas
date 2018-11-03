
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.artists import Artist
from compas_blender.artists.mixins import VertexArtist
from compas_blender.artists.mixins import EdgeArtist
from compas_blender.artists.mixins import FaceArtist


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'VolMeshArtist',
]


class VolMeshArtist(FaceArtist, EdgeArtist, VertexArtist, Artist):

    __module__ = "compas_blender.artists"

    def __init__(self, volmesh, layer=None):
        super(VolMeshArtist, self).__init__(layer=layer)

        pass


    @property
    def volmesh(self):

        raise NotImplementedError


    @volmesh.setter
    def volmesh(self, volmesh):

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
