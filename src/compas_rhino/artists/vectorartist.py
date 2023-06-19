from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import Point
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import RhinoArtist


class VectorArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`
        A COMPAS vector.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`PrimitiveArtist`.

    """

    def __init__(self, vector, layer=None, **kwargs):
        super(VectorArtist, self).__init__(primitive=vector, layer=layer, **kwargs)

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
            If True, draw the base point of the vector.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        color = color.rgb255
        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.primitive
        start = list(start)
        end = list(end)
        guids = []
        if show_point:
            points = [{"pos": start, "color": color, "name": self.primitive.name}]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [
            {
                "start": start,
                "end": end,
                "arrow": "end",
                "color": color,
                "name": self.primitive.name,
            }
        ]
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids
