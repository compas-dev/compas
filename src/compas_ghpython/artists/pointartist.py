from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython.utilities
from compas.artists import PrimitiveArtist
from .artist import GHArtist


class PointArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`
        A COMPAS point.
    """

    def __init__(self, point, **kwargs):
        super(PointArtist, self).__init__(primitive=point, **kwargs)

    def draw(self):
        """Draw the point.

        Returns
        -------
        :class:`Rhino.Geometry.Point3d`
        """
        points = [self._get_args(self.primitive)]
        return compas_ghpython.utilities.draw_points(points)[0]

    @staticmethod
    def _get_args(primitive):
        return {'pos': list(primitive)}
