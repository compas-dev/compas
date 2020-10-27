from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import compas_rhino
from ._primitiveartist import PrimitiveArtist


__all__ = ['PlaneArtist']


class PlaneArtist(PrimitiveArtist):
    """Artist for drawing planes.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Plane`
        A COMPAS plane.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the plane.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
