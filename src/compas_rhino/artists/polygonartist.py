from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import PrimitiveArtist
from .artist import RhinoArtist


class PolygonArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A COMPAS polygon.
    layer : str, optional
        The name of the layer that will contain the mesh.
    """

    def __init__(self, polygon, layer=None):
        super(PolygonArtist, self).__init__(polygon)
        self.layer = layer

    def draw(self, show_points=False, show_edges=False, show_face=True):
        """Draw the polygon.

        Parameters
        ----------
        show_points : bool, optional
            Default is ``False``.
        show_edges : bool, optional
            Default is ``False``.
        show_face : bool, optional
            Default is ``True``.

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
        if show_edges:
            lines = [{'start': list(a), 'end': list(b), 'color': self.color, 'name': self.primitive.name} for a, b in self.primitive.lines]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        if show_face:
            polygons = [{'points': _points, 'color': self.color, 'name': self.primitive.name}]
            guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        return guids
