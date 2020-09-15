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
        polylines = [self._get_args(self.primitive)]
        return compas_ghpython.draw_polylines(polylines)

    @staticmethod
    def draw_collection(collection):
        """Draw a collection of polylines.

        Parameters
        ----------
        collection : list of compas.geometry.Polyline
            A collection of ``Polyline`` objects.

        Returns
        -------
        list of :class:`Rhino.Geometry.Polyline`

        """
        polylines = [PolylineArtist._get_args(primitive) for primitive in collection]
        return compas_ghpython.draw_polylines(polylines)

    @staticmethod
    def _get_args(primitive):
        return {'points': map(list, primitive.points)}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
