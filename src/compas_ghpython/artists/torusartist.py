from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class TorusArtist(GHArtist, GeometryArtist):
    """Artist for drawing torus shapes.

    Parameters
    ----------
    torus : :class:`~compas.geometry.Torus`
        A COMPAS torus.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, torus, **kwargs):
        super(TorusArtist, self).__init__(geometry=torus, **kwargs)

    def draw(self):
        """Draw the torus associated with the artist.

        Returns
        -------
        :rhino:`Rhino.Geometry.Torus`

        """
        geometry = conversions.torus_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        return geometry
