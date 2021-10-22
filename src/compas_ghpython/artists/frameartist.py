from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from .artist import GHArtist


class FrameArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        A COMPAS frame.
    scale : float, optional
        The scale of the vectors representing the axes of the frame.
        Default is ``1.0``.

    Attributes
    ----------
    scale : float
        Scale factor that controls the length of the axes.
        Default is ``1.0``.
    color_origin : tuple of 3 int between 0 and 255
        Default is ``(0, 0, 0)``.
    color_xaxis : tuple of 3 int between 0 and 255
        Default is ``(255, 0, 0)``.
    color_yaxis : tuple of 3 int between 0 and 255
        Default is ``(0, 255, 0)``.
    color_zaxis : tuple of 3 int between 0 and 255
        Default is ``(0, 0, 255)``.
    """

    def __init__(self, frame, scale=1.0, **kwargs):
        super(FrameArtist, self).__init__(primitive=frame, **kwargs)
        self.scale = scale
        self.color_origin = (0, 0, 0)
        self.color_xaxis = (255, 0, 0)
        self.color_yaxis = (0, 255, 0)
        self.color_zaxis = (0, 0, 255)

    def draw(self):
        """Draw the frame.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        return compas_ghpython.draw_frame(self.primitive)

    def draw_origin(self):
        """Draw the frame's origin.

        Returns
        -------
        :class:`Rhino.Geometry.Point`
        """
        point, _ = self._get_args(self.primitive, self.scale, self.color_origin, self.color_xaxis, self.color_yaxis, self.color_zaxis)
        return compas_ghpython.draw_points([point])[0]

    def draw_axes(self):
        """Draw the frame's axes.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`
        """
        _, lines = self._get_args(self.primitive, self.scale, self.color_origin, self.color_xaxis, self.color_yaxis, self.color_zaxis)
        return compas_ghpython.draw_lines(lines)

    @staticmethod
    def _get_args(primitive, scale=1.0, color_origin=(0, 0, 0), color_xaxis=(255, 0, 0), color_yaxis=(0, 255, 0), color_zaxis=(0, 0, 255)):
        origin = list(primitive.point)
        x = list(primitive.point + primitive.xaxis.scaled(scale))
        y = list(primitive.point + primitive.yaxis.scaled(scale))
        z = list(primitive.point + primitive.zaxis.scaled(scale))
        point = {'pos': origin, 'color': color_origin}
        lines = [
            {'start': origin, 'end': x, 'color': color_xaxis, 'arrow': 'end'},
            {'start': origin, 'end': y, 'color': color_yaxis, 'arrow': 'end'},
            {'start': origin, 'end': z, 'color': color_zaxis, 'arrow': 'end'}]
        return point, lines
