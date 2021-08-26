from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['PolylineArtist']


class PolylineArtist(PrimitiveArtist):

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        str
            The GUIDs of the created Rhino object.
        """
        _points = map(list, self.primitive.points)
        # guids = []
        # if show_points:
        #     points = [{'pos': point, 'color': self.color, 'name': self.name} for point in _points]
        #     guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        polylines = [{'points': _points, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_polylines(polylines, layer=self.layer, clear=False, redraw=False)
        return guids[0]
