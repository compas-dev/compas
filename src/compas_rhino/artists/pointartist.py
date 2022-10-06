from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import RhinoArtist


class PointArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`PrimitiveArtist`.

    """

    def __init__(self, point, layer=None, **kwargs):
        super(PointArtist, self).__init__(primitive=point, layer=layer, **kwargs)

    def draw(self, color=None):
        """Draw the point.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the point.
            Default is :attr:`compas.artists.PrimitiveArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        points = [
            {
                "pos": list(self.primitive),
                "color": color.rgb255,
                "name": self.primitive.name,
            }
        ]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        return guids
