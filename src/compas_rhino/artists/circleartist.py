from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists.primitiveartist import PrimitiveArtist


__all__ = ['CircleArtist']


class CircleArtist(PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Circle`
        A COMPAS circle.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    >>>

    """

    def draw(self):
        """Draw the circle.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        point = list(self.primitive.plane.point)
        normal = list(self.primitive.plane.normal)
        radius = self.primitive.radius
        circles = [{'plane': [point, normal], 'radius': radius, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_circles(circles, layer=self.layer, clear=False, redraw=False)
        self.guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
