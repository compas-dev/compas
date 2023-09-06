from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import frame_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from .artist import GHArtist


class FrameArtist(GHArtist, GeometryArtist):
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
        super(FrameArtist, self).__init__(geometry=frame, **kwargs)
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
        return frame_to_rhino(self.geometry)

    def draw_origin(self):
        """Draw the frame's origin.

        Returns
        -------
        :rhino:`Rhino.Geometry.Point`

        """
        return point_to_rhino(self.geometry.point)

    def draw_axes(self):
        """Draw the frame's axes.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        origin = self.geometry.point
        x = self.geometry.point + self.geometry.xaxis * self.scale
        y = self.geometry.point + self.geometry.yaxis * self.scale
        z = self.geometry.point + self.geometry.zaxis * self.scale
        return [
            line_to_rhino([origin, x]),
            line_to_rhino([origin, y]),
            line_to_rhino([origin, z]),
        ]
