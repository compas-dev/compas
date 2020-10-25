from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
import compas_rhino
from ._primitiveartist import PrimitiveArtist


__all__ = ['VectorArtist']


class VectorArtist(PrimitiveArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Vector`
        A COMPAS vector.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Vector
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import VectorArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)

        compas_rhino.clear_layer("Test::VectorArtist")

        for point in pcl.points:
            vector = Vector(0, 0, 1)
            artist = VectorArtist(vector, color=i_to_rgb(random.random()), layer="Test::VectorArtist")
            artist.draw(point=point)

    """

    def draw(self, point=None, show_point=False):
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] or :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_points : bool, optional
            Show the point of application of the vector.
            Default is ``False``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not point:
            point = [0, 0, 0]
        start = Point(*point)
        end = start + self.primitive
        start = list(start)
        end = list(end)
        guids = []
        if show_point:
            points = [{'pos': start, 'color': self.color, 'name': self.name}]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [{'start': start, 'end': end, 'arrow': 'end', 'color': self.color, 'name': self.name}]
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
