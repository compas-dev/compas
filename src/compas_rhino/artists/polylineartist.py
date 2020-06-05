from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
# from compas.utilities import iterable_like
from compas_rhino.artists import PrimitiveArtist


__all__ = ['PolylineArtist']


class PolylineArtist(PrimitiveArtist):
    """Artist for drawing ``Polyline`` objects.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`
        A COMPAS polyline.
    layer : str (optional)
        The name of the layer that will contain the polyline.
        Default value is ``None``, in which case the current layer will be used.

    Examples
    --------
    >>>

    """

    def draw(self):
        """Draw the polyline.

        """
        polylines = [{'points': map(list, self.primitive.points), 'color': self.color, 'name': self.name}]
        self.guids = compas_rhino.draw_polylines(polylines, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
