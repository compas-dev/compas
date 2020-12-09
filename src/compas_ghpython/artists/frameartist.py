from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas_ghpython.artists._primitiveartist import PrimitiveArtist


__all__ = ['FrameArtist']


class FrameArtist(PrimitiveArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame : compas.geometry.Frame
        A COMPAS frame.
    name : str, optional
        The name of the frame.
    scale : float, optional
        The scale of the vectors representing the axes of the frame.
        Default is ``1.0``.

    Attributes
    ----------
    scale : float
    color_origin : tuple of 3 int between 0 abd 255
    color_xaxis : tuple of 3 int between 0 abd 255
    color_yaxis : tuple of 3 int between 0 abd 255
    color_zaxis : tuple of 3 int between 0 abd 255

    Examples
    --------
    >>>

    """

    def __init__(self, frame, scale=1.0):
        super(FrameArtist, self).__init__(frame)
        self.scale = scale
        self.color_origin = (0, 0, 0)
        self.color_xaxis = (255, 0, 0)
        self.color_yaxis = (0, 255, 0)
        self.color_zaxis = (0, 0, 255)

    def draw(self):
        """Draw the frame.

        Returns
        -------
        geometry : list

            * geometry[0] : :class:`Rhino.Geometry.Point`
            * geometry[1] : list of :class:`Rhino.Geometry.Line`

        """
        point, lines = self._get_args(self.primitive, self.scale, self.color_origin, self.color_xaxis, self.color_yaxis, self.color_zaxis)
        geometry = [None, None]
        geometry[0] = compas_ghpython.draw_points([point])
        geometry[1] = compas_ghpython.draw_lines(lines)
        return geometry

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
