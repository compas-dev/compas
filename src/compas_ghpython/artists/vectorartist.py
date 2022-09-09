from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_ghpython
from compas.artists import PrimitiveArtist
from compas.geometry import Point
from compas.colors import Color

from .artist import GHArtist


class VectorArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`
        A COMPAS vector.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, vector, **kwargs):
        super(VectorArtist, self).__init__(primitive=vector, **kwargs)

    def draw(self, color=None, point=None, show_point=False):
        """Draw the vector.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the vector.
            Default is :attr:`compas.artists.PrimitiveArtist.color`.
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_point : bool, optional
            If True, draw the point of application of the vector.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`]
            The Rhino line and endpoints, if requested.

        """
        color = Color.coerce(color) or self.color
        color = color.rgb255
        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.primitive
        start = list(start)
        end = list(end)
        result = []
        if show_point:
            points = [{"pos": start, "color": color, "name": self.primitive.name}]
            result += compas_ghpython.draw_points(points)
        lines = [
            {
                "start": start,
                "end": end,
                "arrow": "end",
                "color": color,
                "name": self.primitive.name,
            }
        ]
        result += compas_ghpython.draw_lines(lines)
        return result
