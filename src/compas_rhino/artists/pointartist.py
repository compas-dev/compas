from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['PointArtist']


class PointArtist(PrimitiveArtist):

    def draw(self):
        """Draw the point.

        Returns
        -------
        str
            The GUID of the created Rhino object.

        """
        points = [{'pos': list(self.primitive), 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        return guids[0]
