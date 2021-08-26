from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['VectorArtist']


class VectorArtist(PrimitiveArtist):

    def draw(self, point=None):
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] or :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

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
        # guids = []
        # if show_point:
        #     points = [{'pos': start, 'color': self.color, 'name': self.name}]
        #     guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [{'start': start, 'end': end, 'arrow': 'end', 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids[0]
