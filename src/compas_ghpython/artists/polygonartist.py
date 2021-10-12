from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from .artist import GHArtist


class PolygonArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A COMPAS polygon.
    """

    def __init__(self, polygon, **kwargs):
        super(PolygonArtist, self).__init__(primitive=polygon, **kwargs)

    def draw(self, show_points=False, show_edges=False, show_face=True):
        """Draw the polygon.

        Parameters
        ----------
        show_points : bool, optional
            Default is ``False``.
        show_edges : bool, optional
            Default is ``False``.
        show_face : bool, optional
            Default is ``True``.

        Returns
        -------
        list
            The Rhino points, lines and faces.
        """
        _points = map(list, self.primitive.points)
        result = []
        if show_points:
            points = [{'pos': point, 'color': self.color, 'name': self.primitive.name} for point in _points]
            result += compas_ghpython.draw_points(points)
        if show_edges:
            lines = [{'start': list(a), 'end': list(b), 'color': self.color, 'name': self.primitive.name} for a, b in self.primitive.lines]
            result += compas_ghpython.draw_lines(lines)
        if show_face:
            polygons = [{'points': _points, 'color': self.color, 'name': self.primitive.name}]
            result += compas_ghpython.draw_faces(polygons)
        return result
