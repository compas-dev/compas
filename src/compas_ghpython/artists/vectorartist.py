from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_ghpython
from compas.artists import PrimitiveArtist
from compas.geometry import Point

from .artist import GHArtist


class VectorArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`
        A COMPAS vector.
    """

    def __init__(self, vector, **kwargs):
        super(VectorArtist, self).__init__(primitive=vector, **kwargs)

    def draw(self, point=None, show_point=False):
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] or :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

        Returns
        -------
        list
            The Rhino lines.

        """
        if not point:
            point = [0, 0, 0]
        start = Point(*point)
        end = start + self.primitive
        start = list(start)
        end = list(end)
        result = []
        if show_point:
            points = [{'pos': start, 'color': self.color, 'name': self.primitive.name}]
            result += compas_ghpython.draw_points(points)
        lines = [{'start': start, 'end': end, 'arrow': 'end', 'color': self.color, 'name': self.primitive.name}]
        result += compas_ghpython.draw_lines(lines)
        return result
