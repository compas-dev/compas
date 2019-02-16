
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.artists import Artist
from compas_blender.artists.mixins import VertexArtist
from compas_blender.artists.mixins import EdgeArtist
from compas_blender.artists.mixins import FaceArtist


__all__ = [
    'VolMeshArtist',
]


class VolMeshArtist(FaceArtist, EdgeArtist, VertexArtist, Artist):

    __module__ = "compas_blender.artists"


    def __init__(self, volmesh, layer=None):
        super(VolMeshArtist, self).__init__(layer=layer)

        self.volmesh = volmesh
        self.defaults.update({
            'color.vertex': [255, 255, 255],
            'color.edge':   [0, 0, 0],
            'color.face':   [110, 110, 110],
        })


    @property
    def volmesh(self):

        return self.datastructure


    @volmesh.setter
    def volmesh(self, volmesh):

        self.datastructure = volmesh


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

    from compas.datastructures import VolMesh


    volmesh = VolMesh.from_obj(compas.get('boxes.obj'))

    artist = VolMeshArtist(volmesh, layer='VolMeshArtist')

    # artist.clear_layer()

    artist.draw_vertices()
    artist.draw_vertexlabels()
    # artist.clear_vertexlabels()

    artist.draw_edges()
    artist.draw_edgelabels()
    # artist.clear_edgelabels()
