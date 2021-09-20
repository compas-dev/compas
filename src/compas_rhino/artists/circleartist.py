from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import add_vectors
from compas.artists import PrimitiveArtist
from .artist import RhinoArtist


class CircleArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`
        A COMPAS circle.
    layer : str, optional
        The layer that should contain the drawing.
    """

    def __init__(self, circle, layer=None):
        super(CircleArtist, self).__init__(circle)
        self.layer = layer

    def draw(self, show_point=False, show_normal=False):
        """Draw the circle.

        Parameters
        ----------
        show_point : bool, optional
            Default is ``False``.
        show_normal : bool, optional
            Default is ``False``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        point = list(self.primitive.plane.point)
        normal = list(self.primitive.plane.normal)
        plane = point, normal
        radius = self.primitive.radius
        guids = []
        if show_point:
            points = [{'pos': point, 'color': self.color, 'name': self.primitive.name}]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        if show_normal:
            lines = [{'start': point, 'end': add_vectors(point, normal), 'arrow': 'end', 'color': self.color, 'name': self.primitive.name}]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        circles = [{'plane': plane, 'radius': radius, 'color': self.color, 'name': self.primitive.name}]
        guids += compas_rhino.draw_circles(circles, layer=self.layer, clear=False, redraw=False)
        return guids
