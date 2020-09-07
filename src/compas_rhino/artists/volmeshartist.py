from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.artists._artist import BaseArtist


__all__ = ['VolMeshArtist']


class VolMeshArtist(BaseArtist):
    """A volmesh artist defines functionality for visualising COMPAS volmeshes in Rhino.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.
    layer : str, optional
        The name of the layer that will contain the volmesh.

    Attributes
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the artist.
    layer : str
        The layer in which the volmesh should be contained.
    color_vertices : 3-tuple
        Default color of the vertices.
    color_edges : 3-tuple
        Default color of the edges.
    color_faces : 3-tuple
        Default color of the faces.

    """

    def __init__(self, volmesh, layer=None):
        super(VolMeshArtist, self).__init__()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
