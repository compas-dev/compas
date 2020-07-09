from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists import PrimitiveArtist


__all__ = ['FrameArtist']


class FrameArtist(PrimitiveArtist):
    """Artist for drawing ``Frame`` objects.

    Parameters
    ----------
    frame : compas.geometry.Frame
        A COMPAS frame.
    layer : str, optional
        The name of the layer that will contain the frame.
        Default value is ``None``, in which case the current layer will be used.
    name : str, optional
        The name of the frame.
    scale : float, optional
        The scale of the vectors representing the axes of the frame.
        Default is ``1.0``.

    Attributes
    ----------


    Examples
    --------
    >>>

    """

    def __init__(self, frame, layer=None, name=None, scale=1.0):
        super(FrameArtist, self).__init__(frame, layer=layer, name=name)
        self.scale = scale
        self.color_origin = (0, 0, 0)
        self.color_xaxis = (255, 0, 0)
        self.color_yaxis = (0, 255, 0)
        self.color_zaxis = (0, 0, 255)

    def draw(self):
        """Draw the frame.

        Returns
        -------
        guids: list
            The GUIDs of the created Rhino objects.

        """
        points = []
        lines = []
        origin = list(self.primitive.point)
        x = list(self.primitive.point + self.primitive.xaxis.scaled(self.scale))
        y = list(self.primitive.point + self.primitive.yaxis.scaled(self.scale))
        z = list(self.primitive.point + self.primitive.zaxis.scaled(self.scale))
        points = [{'pos': origin, 'color': self.color_origin}]
        lines = [
            {'start': origin, 'end': x, 'color': self.color_xaxis, 'arrow': 'end'},
            {'start': origin, 'end': y, 'color': self.color_yaxis, 'arrow': 'end'},
            {'start': origin, 'end': z, 'color': self.color_zaxis, 'arrow': 'end'}]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
