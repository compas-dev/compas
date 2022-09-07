from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from compas.colors import Color
from .artist import GHArtist


class FrameArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`
        A COMPAS frame.
    scale : float, optional
        The scale of the vectors representing the axes of the frame.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    Attributes
    ----------
    scale : float
        Scale factor that controls the length of the axes.
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
        super(FrameArtist, self).__init__(primitive=frame, **kwargs)
        self.scale = scale
        self.color_origin = Color.black()
        self.color_xaxis = Color.red()
        self.color_yaxis = Color.green()
        self.color_zaxis = Color.blue()

    def draw(self):
        """Draw the frame.

        Returns
        -------
        :rhino:`Rhino.Geometry.Plane`

        """
        return compas_ghpython.draw_frame(self.primitive)

    def draw_origin(self):
        """Draw the frame's origin.

        Returns
        -------
        :rhino:`Rhino.Geometry.Point`

        """
        point = {"pos": list(self.primitive.point), "color": self.color_origin.rgb255}
        return compas_ghpython.draw_points([point])[0]

    def draw_axes(self):
        """Draw the frame's axes.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        origin = list(self.primitive.point)
        x = list(self.primitive.point + self.primitive.xaxis.scaled(self.scale))
        y = list(self.primitive.point + self.primitive.yaxis.scaled(self.scale))
        z = list(self.primitive.point + self.primitive.zaxis.scaled(self.scale))
        lines = [
            {
                "start": origin,
                "end": x,
                "color": self.color_xaxis.rgb255,
                "arrow": "end",
            },
            {
                "start": origin,
                "end": y,
                "color": self.color_yaxis.rgb255,
                "arrow": "end",
            },
            {
                "start": origin,
                "end": z,
                "color": self.color_zaxis.rgb255,
                "arrow": "end",
            },
        ]
        return compas_ghpython.draw_lines(lines)
