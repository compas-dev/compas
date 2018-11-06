from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas_ghpython.artists.mixins import VertexArtist
from compas_ghpython.artists.mixins import EdgeArtist
from compas_ghpython.artists.mixins import FaceArtist


__all__ = ['VolMeshArtist']


class VolMeshArtist(FaceArtist, EdgeArtist, VertexArtist):
    """A volmesh artist defines functionality for visualising COMPAS volmeshes in GhPython.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A COMPAS volmesh.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, volmesh):
        self.volmesh = volmesh
        self.defaults = {
            'color.vertex' : (255, 255, 255),
            'color.edge'   : (0, 0, 0),
            'color.face'   : (210, 210, 210),
        }

    @property
    def volmesh(self):
        """compas.datastructures.VolMesh: The volmesh that should be painted."""
        return self.datastructure

    @volmesh.setter
    def volmesh(self, volmesh):
        self.datastructure = volmesh

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    import compas

    from compas.datastructures import VolMesh
    from compas_ghpython.artists.volmeshartist import VolMeshArtist

    volmesh = VolMesh.from_obj(compas.get('boxes.obj'))

    artist = VolMeshArtist(volmesh)

    vertices = artist.draw_vertices()
    faces = artist.draw_faces()
    edges = artist.draw_edges()
