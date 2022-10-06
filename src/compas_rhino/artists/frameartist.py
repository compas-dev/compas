from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import RhinoArtist


class FrameArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame: :class:`~compas.geometry.Frame`
        A COMPAS frame.
    scale: float, optional
        Scale factor that controls the length of the axes.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`PrimitiveArtist`.

    Attributes
    ----------
    scale : float
        Scale factor that controls the length of the axes.
        Default is ``1.0``.
    color_origin : :class:`~compas.colors.Color`
        Default is ``Color.black()``.
    color_xaxis : :class:`~compas.colors.Color`
        Default is ``Color.red()``.
    color_yaxis : :class:`~compas.colors.Color`
        Default is ``Color.green()``.
    color_zaxis : :class:`~compas.colors.Color`
        Default is ``Color.blue()``.

    """

    def __init__(self, frame, layer=None, scale=1.0, **kwargs):
        super(FrameArtist, self).__init__(primitive=frame, layer=layer, **kwargs)
        self.scale = scale or 1.0
        self.color_origin = Color.black()
        self.color_xaxis = Color.red()
        self.color_yaxis = Color.green()
        self.color_zaxis = Color.blue()

    def draw(self):
        """Draw the frame.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        points = []
        lines = []
        origin = list(self.primitive.point)
        X = list(self.primitive.point + self.primitive.xaxis.scaled(self.scale))
        Y = list(self.primitive.point + self.primitive.yaxis.scaled(self.scale))
        Z = list(self.primitive.point + self.primitive.zaxis.scaled(self.scale))
        points = [{"pos": origin, "color": self.color_origin.rgb255}]
        lines = [
            {
                "start": origin,
                "end": X,
                "color": self.color_xaxis.rgb255,
                "arrow": "end",
            },
            {
                "start": origin,
                "end": Y,
                "color": self.color_yaxis.rgb255,
                "arrow": "end",
            },
            {
                "start": origin,
                "end": Z,
                "color": self.color_zaxis.rgb255,
                "arrow": "end",
            },
        ]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids
