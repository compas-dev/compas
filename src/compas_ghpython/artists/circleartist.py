from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class CircleArtist(GHArtist, GeometryArtist):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__(geometry=circle, **kwargs)

    def draw(self):
        """Draw the circle.

        Returns
        -------
        :rhino:`Rhino.Geometry.Circle`

        """
        circle = conversions.circle_to_rhino(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            circle.Transform(transformation)

        return circle
