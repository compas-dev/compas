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


__all__ = ['MeshArtist']


class MeshArtist(FaceArtist, EdgeArtist, VertexArtist):
    """"""

    def __init__(self, mesh, layer=0):
        self.datastructure = mesh
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

    from compas_blender.utilities import get_objects

    from compas_blender.helpers import mesh_from_bmesh

    mesh = mesh_from_bmesh(bmesh=get_objects(layer=0)[0])

    meshartist = MeshArtist(mesh=mesh, layer=1)

    meshartist.clear_layer()

    meshartist.draw_vertices()
    meshartist.draw_vertexlabels()
    meshartist.clear_vertices(keys=[4])
    meshartist.clear_vertexlabels(keys=[6])

    meshartist.draw_edges()
    meshartist.draw_edgelabels()
    meshartist.clear_edges(keys=[(0, 4)])
    meshartist.clear_edgelabels(keys=[(5, 4)])

    meshartist.draw_faces()
    meshartist.draw_facelabels()
    meshartist.clear_faces(keys=[2, 3])
    meshartist.clear_facelabels(keys=[5])