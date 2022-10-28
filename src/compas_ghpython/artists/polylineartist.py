from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import GHArtist


class PolylineArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, polyline, **kwargs):
        super(PolylineArtist, self).__init__(primitive=polyline, **kwargs)

    def draw(self, color=None):
        """Draw the polyline.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the polyline.
            Default is :attr:`compas.artists.PrimitiveArtist.color`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Polyline`.

        """
        color = Color.coerce(color) or self.color
        polylines = [{"points": map(list, self.primitive.points), "color": color.rgb255}]
        return compas_ghpython.draw_polylines(polylines)[0]
