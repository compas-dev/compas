from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas_ghpython.artists._primitiveartist import PrimitiveArtist


__all__ = ['PointArtist']


class PointArtist(PrimitiveArtist):
    """Artist for drawing points.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Point`
        A COMPAS point.

    Other Parameters
    ----------------
    See :class:`compas_rhino.artists.PrimitiveArtist` for all other parameters.

    """

    def draw(self):
        """Draw the point.

        Returns
        -------
        :class:`Rhino.Geometry.Point3d`

        """
        points = [{'pos': list(self.primitive)}]
        return compas_ghpython.draw_points(points)[0]

    @staticmethod
    def draw_collection(collection):
        """Draw a collection of points.

        Parameters
        ----------
        collection : list of compas.geometry.Point
            A collection of ``Point`` objects.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        points = [{'pos': list(point)} for point in collection]
        return compas_ghpython.draw_points(points)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
