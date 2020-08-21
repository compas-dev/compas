from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['VectorArtist']


class VectorArtist(PrimitiveArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`
        A COMPAS vector.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    >>>

    """

    def draw(self):
        """Draw the vector.

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
