from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['LineArtist']


class LineArtist(PrimitiveArtist):

    def draw(self):
        """Draw the line.

        Returns
        -------
        str
            The GUID of the created Rhino object.

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        # guids = []
        # if show_points:
        #     points = [
        #         {'pos': start, 'color': self.color, 'name': self.name},
        #         {'pos': end, 'color': self.color, 'name': self.name}
        #     ]
        #     guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [{'start': start, 'end': end, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids[0]
