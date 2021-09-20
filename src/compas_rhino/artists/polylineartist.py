from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import PrimitiveArtist
from .artist import RhinoArtist


class PolylineArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`compas.geometry.Polyline`
        A COMPAS polyline.
    """

    def __init__(self, polyline, layer=None):
        super(PolylineArtist, self).__init__(polyline)
        self.layer = layer

    def draw(self, show_points=False):
        """Draw the polyline.

        Parameters
        ----------
        show_points : bool, optional
            Default is ``False``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        _points = map(list, self.primitive.points)
        guids = []
        if show_points:
            points = [{'pos': point, 'color': self.color, 'name': self.primitive.name} for point in _points]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        polylines = [{'points': _points, 'color': self.color, 'name': self.primitive.name}]
        guids = compas_rhino.draw_polylines(polylines, layer=self.layer, clear=False, redraw=False)
        return guids
