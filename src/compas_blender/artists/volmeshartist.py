import time

try:
    import bpy
except ImportError:
    pass

from compas_blender.utilities import clear_layer
from compas_blender.artists.mixins import VertexArtist
from compas_blender.artists.mixins import EdgeArtist
from compas_blender.artists.mixins import FaceArtist


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['VolMeshArtist']


class VolMeshArtist(FaceArtist, EdgeArtist, VertexArtist):
    """"""

    def __init__(self, volmesh, layer=0):
        self.datastructure = volmesh
        self.layer = layer
        self.defaults = {
            'color.vertex': [1, 0, 0],
            'color.face': [1, 1, 1],
            'color.edge': [0, 0, 1]}

    def redraw(self, timeout=None):
        """Redraw the Blender view."""
        if timeout:
            time.sleep(timeout)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def clear_layer(self):
        clear_layer(layer=self.layer)

    def clear(self):
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
