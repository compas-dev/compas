from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from ._primitiveartist import PrimitiveArtist


__all__ = ['PointArtist']


class PointArtist(PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Point`
        A COMPAS point.

    Notes
    -----
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import PointArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)

        compas_rhino.clear_layer("Test::PointArtist")

        for point in pcl.points:
            artist = PointArtist(point, color=i_to_rgb(random.random()), layer="Test::PointArtist")
            artist.draw()

    """

    def draw(self):
        """Draw the point.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        points = [{'pos': list(self.primitive), 'color': self.color, 'name': self.name}]
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
