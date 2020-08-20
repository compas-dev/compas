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
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the artist.
    layer : str
        The layer in which the volmesh should be contained.
    settings : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, volmesh, layer=None, settings=None):
        super(VolMeshArtist, self).__init__(volmesh, layer=layer, settings=settings)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
