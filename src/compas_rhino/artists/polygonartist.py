from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from ._primitiveartist import PrimitiveArtist


__all__ = ['PolygonArtist']


class PolygonArtist(PrimitiveArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Polygon`
        A COMPAS polygon.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Polygon
        from compas.geometry import Translation
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import PolygonArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        tpl = Polygon.from_sides_and_radius_xy(7, 0.8)

        compas_rhino.clear_layer("Test::PolygonArtist")

        for point in pcl.points:
            polygon = tpl.transformed(Translation.from_vector(point))
            artist = PolygonArtist(polygon, color=i_to_rgb(random.random()), layer="Test::PolygonArtist")
            artist.draw()

    """

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
            points = [{'pos': point, 'color': self.color, 'name': self.name} for point in _points]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        if show_edges:
            lines = [{'start': list(a), 'end': list(b), 'color': self.color, 'name': self.name} for a, b in self.primitive.lines]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        if show_face:
            polygons = [{'points': _points, 'color': self.color, 'name': self.name}]
            guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
