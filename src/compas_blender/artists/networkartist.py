import time

try:
    import bpy
except ImportError:
    pass

from compas_blender.utilities import clear_layer
from compas_blender.artists.mixins import VertexArtist
from compas_blender.artists.mixins import EdgeArtist
from compas_blender.artists.mixins import PathArtist


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['NetworkArtist']


class NetworkArtist(PathArtist, EdgeArtist, VertexArtist):
    """"""

    def __init__(self, network, layer=0):
        self.datastructure = network
        self.layer = layer
        self.defaults = {
            'color.vertex': [1, 0, 0],
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
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import get_objects

    from compas_blender.helpers import network_from_bmesh

    network = network_from_bmesh(bmesh=get_objects(layer=0)[0])

    networkartist = NetworkArtist(network=network, layer=1)

    networkartist.clear_layer()

    networkartist.draw_vertices()
    networkartist.draw_vertexlabels()
    networkartist.clear_vertices(keys=[4])
    networkartist.clear_vertexlabels(keys=[6])

    networkartist.draw_edges()
    networkartist.draw_edgelabels()
    networkartist.clear_edges(keys=[(0, 4)])
    networkartist.clear_edgelabels(keys=[(5, 4)])
