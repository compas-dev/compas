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
    layer : str (optional)
        The name of the layer that will contain the frame.
        Default value is ``None``, in which case the current layer will be used.

    Examples
    --------
    >>>

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, frame, layer=None, scale=1.0):
        super(FrameArtist, self).__init__(frame, layer=layer)
        self.settings.update({
            'color.origin': (0, 0, 0),
            'color.xaxis': (255, 0, 0),
            'color.yaxis': (0, 255, 0),
            'color.zaxis': (0, 0, 255)})
        self.scale = scale

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
        points = [{'pos': origin, 'color': self.settings['color.origin']}]
        lines = [
            {'start': origin, 'end': x, 'color': self.settings['color.xaxis'], 'arrow': 'end'},
            {'start': origin, 'end': y, 'color': self.settings['color.yaxis'], 'arrow': 'end'},
            {'start': origin, 'end': z, 'color': self.settings['color.zaxis'], 'arrow': 'end'}]
        guids = compas_rhino.draw_points(points, layer=self.settings['layer'], clear=False)
        guids += compas_rhino.draw_lines(lines, layer=self.settings['layer'], clear=False)
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
