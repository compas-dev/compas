from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import GeometryArtist
from compas.colors import Color
from .artist import RhinoArtist


class PolygonArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        A COMPAS polygon.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, polygon, **kwargs):
        super(PolygonArtist, self).__init__(geometry=polygon, **kwargs)

    def draw(self, color=None, show_points=False, show_edges=False, show_face=True):
        """Draw the polygon.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the polygon.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        show_points : bool, optional
            If True, draw the corner points of the polygon.
        show_edges : bool, optional
            If True, draw the boundary edges of the polygon.
        show_face : bool, optional
            If True, draw the face of the polygon.

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

        if show_edges:
            lines = [
                {
                    "start": list(a),
                    "end": list(b),
                    "color": color,
                    "name": self.geometry.name,
                }
                for a, b in self.geometry.lines
            ]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

        if show_face:
            polygons = [{"points": _points, "color": color, "name": self.geometry.name}]
            guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)

        return guids
