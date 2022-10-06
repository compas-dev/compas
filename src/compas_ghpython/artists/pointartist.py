from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython.utilities
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import GHArtist


class PointArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, point, **kwargs):
        super(PointArtist, self).__init__(primitive=point, **kwargs)

    def draw(self, color=None):
        """Draw the point.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the point.
            Default is :attr:`compas.artists.PrimitiveArtist.color`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Point3d`

        """
        color = Color.coerce(color) or self.color
        points = [{"pos": list(self.primitive), "color": color.rgb255}]
        return compas_ghpython.utilities.draw_points(points)[0]
