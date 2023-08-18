from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import GeometryArtist
from compas.colors import Color
from .artist import RhinoArtist


class PolylineArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, polyline, **kwargs):
        super(PolylineArtist, self).__init__(geometry=polyline, **kwargs)

    def draw(self, color=None, show_points=False):
        """Draw the polyline.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the polyline.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        show_points : bool, optional
            If True, draw the points of the polyline.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        color = color.rgb255  # type: ignore
        _points = map(list, self.geometry.points)

        guids = []

        if show_points:
            points = [{"pos": point, "color": color, "name": self.geometry.name} for point in _points]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

        polylines = [{"points": _points, "color": color, "name": self.geometry.name}]
        guids += compas_rhino.draw_polylines(polylines, layer=self.layer, clear=False, redraw=False)

        return guids
