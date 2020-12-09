from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas_ghpython.artists._primitiveartist import PrimitiveArtist


__all__ = ['CircleArtist']


class CircleArtist(PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Circle`
        A COMPAS circle.

    Other Parameters
    ----------------
    See :class:`compas_ghpython.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the circle.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`

        """
        circles = [self._get_args(self.primitive)]
        return compas_ghpython.draw_circles(circles)[0]

    @staticmethod
    def _get_args(primitive):
        point = list(primitive.plane.point)
        normal = list(primitive.plane.normal)
        radius = primitive.radius
        return {'plane': [point, normal], 'radius': radius, 'color': None, 'name': primitive.name}


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
