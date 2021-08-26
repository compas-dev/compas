from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['PolygonArtist']


class PolygonArtist(PrimitiveArtist):

    def draw(self):
        """Draw the polygon.

        Returns
        -------
        str
            The GUID of the created Rhino object.
        """
        _points = map(list, self.primitive.points)
        # guids = []
        # if show_points:
        #     points = [{'pos': point, 'color': self.color, 'name': self.name} for point in _points]
        #     guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        # if show_edges:
        #     lines = [{'start': list(a), 'end': list(b), 'color': self.color, 'name': self.name} for a, b in self.primitive.lines]
        #     guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        # if show_face:
        polygons = [{'points': _points, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        return guids[0]
