from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class BoxArtist(GHArtist, GeometryArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, box, **kwargs):
        super(BoxArtist, self).__init__(geometry=box, **kwargs)

    def draw(self):
        """Draw the box associated with the artist.

        Returns
        -------
        :rhino:`Rhino.Geometry.Box`

        """
        box = conversions.box_to_rhino(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            box.Transform(transformation)

        return box
