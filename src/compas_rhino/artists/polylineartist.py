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
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`PrimitiveArtist`.

    """

    def __init__(self, polyline, layer=None, **kwargs):
        super(PolylineArtist, self).__init__(primitive=polyline, layer=layer, **kwargs)

    def draw(self, show_points=False):
        """Draw the polyline.

        Parameters
        ----------
        show_points : bool, optional
            If True, draw the points of the polyline.

        Returns
        -------
        list[System.Guid]
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
