from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import add_vectors
from compas.artists import GeometryArtist
from compas.colors import Color
from .artist import RhinoArtist


class CircleArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__(geometry=circle, **kwargs)

    def draw(self, color=None, show_point=False, show_normal=False):
        """Draw the circle.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the circle.
            Default is :attr:`compas.artists.GeometryArtist.color`.
        show_point : bool, optional
            If True, draw the center point of the circle.
        show_normal : bool, optional
            If True, draw the normal vector of the circle.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        color = color.rgb255  # type: ignore
        point = list(self.geometry.plane.point)
        normal = list(self.geometry.plane.normal)
        plane = point, normal
        radius = self.geometry.radius

        guids = []

        if show_point:
            points = [{"pos": point, "color": color, "name": self.geometry.name}]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

        if show_normal:
            lines = [
                {
                    "start": point,
                    "end": add_vectors(point, normal),
                    "arrow": "end",
                    "color": color,
                    "name": self.geometry.name,
                }
            ]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

        circles = [{"plane": plane, "radius": radius, "color": color, "name": self.geometry.name}]
        guids += compas_rhino.draw_circles(circles, layer=self.layer, clear=False, redraw=False)

        return guids
