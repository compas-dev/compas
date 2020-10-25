from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from ._primitiveartist import PrimitiveArtist


__all__ = ['PolylineArtist']


class PolylineArtist(PrimitiveArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Polyline`
        A COMPAS polyline.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Polyline
        from compas.geometry import Translation
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import PolylineArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        tpl = Polyline(Polygon.from_sides_and_radius_xy(7, 0.8).points)

        compas_rhino.clear_layer("Test::PolylineArtist")

        for point in pcl.points:
            polyline = tpl.transformed(Translation.from_vector(point))
            artist = PolylineArtist(polygon, color=i_to_rgb(random.random()), layer="Test::PolylineArtist")
            artist.draw()

    """

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
            points = [{'pos': point, 'color': self.color, 'name': self.name} for point in _points]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        polylines = [{'points': _points, 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_polylines(polylines, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
