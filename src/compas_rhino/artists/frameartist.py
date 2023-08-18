from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import GeometryArtist
from compas.colors import Color
from .artist import RhinoArtist


class FrameArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame: :class:`~compas.geometry.Frame`
        A COMPAS frame.
    scale: float, optional
        Scale factor that controls the length of the axes.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

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

    def __init__(self, frame, scale=1.0, **kwargs):
        super(FrameArtist, self).__init__(geometry=frame, **kwargs)
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

        origin = list(self.geometry.point)
        X = list(self.geometry.point + self.geometry.xaxis.scaled(self.scale))
        Y = list(self.geometry.point + self.geometry.yaxis.scaled(self.scale))
        Z = list(self.geometry.point + self.geometry.zaxis.scaled(self.scale))

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
