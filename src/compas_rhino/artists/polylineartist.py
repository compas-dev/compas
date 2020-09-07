from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['PolylineArtist']


class PolylineArtist(PrimitiveArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Polyline`
        A COMPAS polyline.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        polylines = [{'points': map(list, self.primitive.points), 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_polylines(polylines, layer=self.layer, clear=False, redraw=False)
        self.guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
