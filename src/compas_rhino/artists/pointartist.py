from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import GeometryArtist
from compas.colors import Color
from .artist import RhinoArtist


class PointArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, point, **kwargs):
        super(PointArtist, self).__init__(geometry=point, **kwargs)

    def draw(self, color=None):
        """Draw the point.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the point.
            Default is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        points = [
            {
                "pos": list(self.geometry),
                "color": color.rgb255,  # type: ignore
                "name": self.geometry.name,
            }
        ]

        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        return guids
