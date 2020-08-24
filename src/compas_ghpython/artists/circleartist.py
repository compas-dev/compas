from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas_ghpython.artists._primitiveartist import PrimitiveArtist


__all__ = ['CircleArtist']


class CircleArtist(PrimitiveArtist):
    """Artist for drawing circles.

    Examples
    --------
    .. code-block:: python

        from compas.geometry import Circle
        from compas.geometry import Plane
        from compas_ghpython.artists import CircleArtist

        circle = Circle(Plane([0,0,0], [1,0,0]), 10)

        artist = CircleArtist(circle)
        a = artist.draw()

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
