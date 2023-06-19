from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import GHArtist


class CircleArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__(primitive=circle, **kwargs)

    def draw(self, color=None):
        """Draw the circle.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The color of the circle.
            Default is :attr:`compas.artists.PrimitiveArtist.color`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Circle`

        """
        color = Color.coerce(color) or self.color
        point = list(self.primitive.plane.point)
        normal = list(self.primitive.plane.normal)
        radius = self.primitive.radius
        circles = [
            {
                "plane": [point, normal],
                "radius": radius,
                "color": color.rgb255,
                "name": self.primitive.name,
            }
        ]
        return compas_ghpython.draw_circles(circles)[0]
