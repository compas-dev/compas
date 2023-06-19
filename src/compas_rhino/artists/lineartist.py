from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import RhinoArtist


class LineArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A COMPAS line.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`PrimitiveArtist`.

    """

    def __init__(self, line, layer=None, **kwargs):
        super(LineArtist, self).__init__(primitive=line, layer=layer, **kwargs)

    def draw(self, color=None, show_points=False):
        """Draw the line.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the line.
            Default is :attr:`compas.artists.PrimitiveArtist.color`.
        show_points : bool, optional
            If True, draw the start and end point of the line.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        color = Color.coerce(color) or self.color
        color = color.rgb255
        guids = []
        if show_points:
            points = [
                {"pos": start, "color": color, "name": self.primitive.name},
                {"pos": end, "color": color, "name": self.primitive.name},
            ]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [{"start": start, "end": end, "color": color, "name": self.primitive.name}]
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids
