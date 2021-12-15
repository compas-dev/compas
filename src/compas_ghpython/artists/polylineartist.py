from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from .artist import GHArtist


class PolylineArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`
        A COMPAS polyline.

    """

    def __init__(self, polyline, **kwargs):
        super(PolylineArtist, self).__init__(primitive=polyline, **kwargs)

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        :class:`Rhino.Geometry.Polyline`.
        """
        polylines = [self._get_args(self.primitive)]
        return compas_ghpython.draw_polylines(polylines)

    @staticmethod
    def _get_args(primitive):
        return {'points': map(list, primitive.points)}
