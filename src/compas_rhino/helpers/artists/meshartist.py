import time

from compas.cad import ArtistInterface

import compas_rhino

from compas_rhino.helpers.artists.mixins import VertexArtist
from compas_rhino.helpers.artists.mixins import EdgeArtist
from compas_rhino.helpers.artists.mixins import FaceArtist

try:
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['MeshArtist']


class MeshArtist(FaceArtist, EdgeArtist, VertexArtist, ArtistInterface):
    """"""

    def __init__(self, mesh, layer=None):
        self.datastructure = mesh
        self.layer = layer
        self.defaults = {
            'color.vertex' : (255, 0, 0),
            'color.face'   : (255, 255, 255),
            'color.edge'   : (0, 0, 0),
        }

    def redraw(self, timeout=None):
        """Redraw the Rhino view."""
        if timeout:
            time.sleep(timeout)
        rs.EnableRedraw(True)
        rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()

    def clear(self):
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.geometry import Polyhedron

    from compas_rhino.helpers.artists.meshartist import MeshArtist

    poly = Polyhedron.generate(12)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    artist = MeshArtist(mesh, layer='MeshArtist')

    artist.clear_layer()

    artist.draw_vertices()
    artist.redraw(0.0)

    artist.draw_vertexlabels()
    artist.redraw(1.0)

    artist.draw_faces()
    artist.redraw(1.0)

    artist.draw_facelabels()
    artist.redraw(1.0)

    artist.draw_edges()
    artist.redraw(1.0)

    artist.draw_edgelabels()
    artist.redraw(1.0)
