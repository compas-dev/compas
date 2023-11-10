from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .artist import GHArtist


class EllipseArtist(GHArtist, GeometryObject):
    """Artist for drawing ellipses.

    Parameters
    ----------
    ellipse : :class:`~compas.geometry.Ellipse`
        A COMPAS ellipse.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, ellipse, **kwargs):
        super(EllipseArtist, self).__init__(geometry=ellipse, **kwargs)

    def draw(self):
        """Draw the ellipse.

        Returns
        -------
        :rhino:`Rhino.Geometry.Ellipse`

        """
        ellipse = conversions.ellipse_to_rhino(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            ellipse.Transform(transformation)

        return ellipse
