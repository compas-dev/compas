from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class ConeArtist(GHArtist, GeometryArtist):
    """Artist for drawing cone shapes.

    Parameters
    ----------
    shape : :class:`~compas.geometry.Cone`
        A COMPAS cone.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cone, **kwargs):
        super(ConeArtist, self).__init__(geometry=cone, **kwargs)

    def draw(self):
        """Draw the cone associated with the artist.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]

        """
        breps = conversions.cone_to_rhino_brep(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            for geometry in breps:
                geometry.Transform(transformation)

        return breps
