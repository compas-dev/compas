from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import add_vectors
from ._primitiveartist import PrimitiveArtist


__all__ = ['CircleArtist']


class CircleArtist(PrimitiveArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Circle`
        A COMPAS circle.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Circle
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import CircleArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        tpl = Circle([[0, 0, 0], [0, -1, 0]], 0.7)

        compas_rhino.clear_layer("Test::CircleArtist")

        for point in pcl.points:
            circle = tpl.copy()
            circle.plane.point = point
            artist = CircleArtist(circle, color=i_to_rgb(random.random()), layer="Test::CircleArtist")
            artist.draw()

    """

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
            points = [{'pos': point, 'color': self.color, 'name': self.name}]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        if show_normal:
            lines = [{'start': point, 'end': add_vectors(point, normal), 'arrow': 'end', 'color': self.color, 'name': self.name}]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        circles = [{'plane': plane, 'radius': radius, 'color': self.color, 'name': self.name}]
        guids += compas_rhino.draw_circles(circles, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
