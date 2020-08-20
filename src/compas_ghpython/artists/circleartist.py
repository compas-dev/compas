from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas_ghpython.artists.primitiveartist import PrimitiveArtist


__all__ = ['CircleArtist']


class CircleArtist(PrimitiveArtist):
    """Artist for drawing circles.

    Examples
    --------
    >>>

    """

    def draw(self):
        """Draw the circle.

        Returns
        -------
        list of :class:`Rhino.Geometry.Circle`

        """
        point = list(self.primitive.plane.point)
        normal = list(self.primitive.plane.normal)
        radius = self.primitive.radius
        circles = [{'plane': [point, normal], 'radius': radius, 'color': self.color, 'name': self.name}]
        return compas_ghpython.draw_circles(circles)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
