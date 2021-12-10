from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
import compas_rhino
from compas.artists import PrimitiveArtist
from .artist import RhinoArtist


class VectorArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`
        A COMPAS vector.
    layer : str, optional
        The layer that should contain the drawing.
    """

    def __init__(self, vector, layer=None, **kwargs):
        super(VectorArtist, self).__init__(primitive=vector, layer=layer, **kwargs)

    def draw(self, point=None, show_point=False):
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] or :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_point : bool, optional
            Show the point of application of the vector.
            Default is ``False``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not point:
            point = [0, 0, 0]
        start = Point(*point)
        end = start + self.primitive
        start = list(start)
        end = list(end)
        guids = []
        if show_point:
            points = [{'pos': start, 'color': self.color, 'name': self.primitive.name}]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [{'start': start, 'end': end, 'arrow': 'end', 'color': self.color, 'name': self.primitive.name}]
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids
