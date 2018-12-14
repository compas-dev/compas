
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
            'color.vertex': (255, 255, 255),
            'color.edge':   (0, 0, 0),
            'color.face':   (210, 210, 210),
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

    from compas.geometry import Polyhedron

    from compas.datastructures import Mesh

    
    poly = Polyhedron.generate(12)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    artist = MeshArtist(mesh)

    #artist.clear()

    artist.draw_vertices(radius=0.01)
    artist.draw_vertexlabels()
    
    artist.draw_edges()
    artist.draw_edgelabels()
    
    # artist.draw_faces()
    # artist.redraw(1.0)

    # artist.draw_facelabels()

    # artist.redraw(1.0)

    # print(artist.save(os.path.join(compas.TEMP, 'test4.png')))
