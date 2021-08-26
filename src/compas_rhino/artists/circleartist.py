from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
# from compas.geometry import add_vectors
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['CircleArtist']


class CircleArtist(PrimitiveArtist):

    def draw(self):
        """Draw the circle.

        Returns
        -------
        str
            The GUID of the created Rhino object.
        """
        point = list(self.primitive.plane.point)
        normal = list(self.primitive.plane.normal)
        plane = point, normal
        radius = self.primitive.radius
        # guids = []
        # if show_point:
        #     points = [{'pos': point, 'color': self.color, 'name': self.name}]
        #     guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        # if show_normal:
        #     lines = [{'start': point, 'end': add_vectors(point, normal), 'arrow': 'end', 'color': self.color, 'name': self.name}]
        #     guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        circles = [{'plane': plane, 'radius': radius, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_circles(circles, layer=self.layer, clear=False, redraw=False)
        # self._guids = guids
        return guids[0]
