from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas_ghpython.artists._primitiveartist import PrimitiveArtist


__all__ = ['PolylineArtist']


class PolylineArtist(PrimitiveArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Polyline`
        A COMPAS polyline.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        :class:`Rhino.Geometry.Polyline`.
        """
        polylines = [{'points': map(list, self.primitive.points)}]
        return compas_ghpython.draw_polylines(polylines)[0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
