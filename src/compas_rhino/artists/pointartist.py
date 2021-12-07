from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import PrimitiveArtist
from .artist import RhinoArtist


class PointArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`
        A COMPAS point.
    layer : str, optional
        The layer that should contain the drawing.
    """

    def __init__(self, point, layer=None, **kwargs):
        super(PointArtist, self).__init__(primitive=point, layer=layer, **kwargs)

    def draw(self):
        """Draw the point.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        points = [{'pos': list(self.primitive), 'color': self.color, 'name': self.primitive.name}]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        return guids
