from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from ._primitiveartist import PrimitiveArtist


__all__ = ['LineArtist']


class LineArtist(PrimitiveArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Line`
        A COMPAS line.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Vector
        from compas.geometry import Line
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import LineArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)

        compas_rhino.clear_layer("Test::LineArtist")

        for point in pcl.points:
            line = Line(point, point + Vector(1, 0, 0))
            artist = LineArtist(line, color=i_to_rgb(random.random()), layer="Test::LineArtist")
            artist.draw()

    """

    def draw(self, show_points=False):
        """Draw the line.

        Parameters
        ----------
        show_points : bool, optional
            Show the start and end point.
            Default is ``False``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        start = list(self.primitive.start)
        end = list(self.primitive.end)
        guids = []
        if show_points:
            points = [
                {'pos': start, 'color': self.color, 'name': self.name},
                {'pos': end, 'color': self.color, 'name': self.name}
            ]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [{'start': start, 'end': end, 'color': self.color, 'name': self.name}]
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
