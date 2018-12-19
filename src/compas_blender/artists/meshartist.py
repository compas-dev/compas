
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
    'MeshArtist',
]


class MeshArtist(FaceArtist, EdgeArtist, VertexArtist, Artist):

    __module__ = "compas_blender.artists"

    def __init__(self, mesh, layer=None):
        super(MeshArtist, self).__init__(layer=layer)

        self.mesh = mesh
        self.defaults.update({
            'color.vertex': [255, 255, 255],
            'color.edge':   [0, 0, 0],
            'color.face':   [110, 110, 110],
        })


    @property
    def mesh(self):

        return self.datastructure


    @mesh.setter
    def mesh(self, mesh):

        self.datastructure = mesh


    def draw(self):

        raise NotImplementedError


    def clear(self):

        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh


    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))

    artist = MeshArtist(mesh)

    # artist.clear()

    # artist.draw_vertices(radius=0.01)
    # artist.draw_vertexlabels()
    # artist.clear_vertexlabels()

    # artist.draw_edges(width=0.01)
    # artist.draw_edgelabels()
    # artist.clear_edgelabels()

    artist.draw_faces()
    # artist.draw_facelabels()
    # artist.clear_facelabels()
