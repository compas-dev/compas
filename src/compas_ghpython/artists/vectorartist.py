from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.artists import GeometryArtist
from compas.geometry import Point
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import point_to_rhino
from .artist import GHArtist


class VectorArtist(GHArtist, GeometryArtist):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`
        A COMPAS vector.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, vector, **kwargs):
        super(VectorArtist, self).__init__(geometry=vector, **kwargs)

    def draw(self, point=None, show_point=False):
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.
        show_point : bool, optional
            If True, draw the point of application of the vector.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`]
            The Rhino line and endpoints, if requested.

        """
        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.geometry

        result = []
        result.append(line_to_rhino([start, end]))

        if show_point:
            result.append(point_to_rhino(start))

        return result
