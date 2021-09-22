from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from .artist import GHArtist


class CircleArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`
        A COMPAS circle.
    """

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__(primitive=circle, **kwargs)

    def draw(self):
        """Draw the circle.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`

        """
        circles = [self._get_args(self.primitive, self.color)]
        return compas_ghpython.draw_circles(circles)[0]

    @staticmethod
    def _get_args(primitive, color=None):
        point = list(primitive.plane.point)
        normal = list(primitive.plane.normal)
        radius = primitive.radius
        return {'plane': [point, normal], 'radius': radius, 'color': color, 'name': primitive.name}
