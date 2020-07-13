from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.artists.meshartist import MeshArtist


__all__ = ['VolMeshArtist']


class VolMeshArtist(MeshArtist):
    """A volmesh artist defines functionality for visualising COMPAS volmeshes in Rhino.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A COMPAS volmesh.
    layer : str, optional
        The name of the layer that will contain the volmesh.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, volmesh, layer=None):
        super(VolMeshArtist, self).__init__(volmesh, layer=layer)

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

    mesh = VolMesh.from_obj(compas.get('boxes.obj'))

    artist = VolMeshArtist(mesh)
    artist.clear()
    artist.draw_faces()
    artist.draw_vertices()
    artist.draw_edges()
