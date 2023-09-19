from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class BrepArtist(GHArtist, GeometryArtist):
    """An artist for drawing a brep in Grasshopper.

    Parameters
    ----------
    brep : :class:`~compas_rhino.geometry.RhinoBrep`
        The brep to draw.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, brep, **kwargs):
        super(BrepArtist, self).__init__(geometry=brep, **kwargs)

    def draw(self):
        """Draw the brep as a Grasshopper geometry.

        Returns
        -------
        :rhino:`Rhino.Geometry.Brep`
            The Grasshopper geometry instance.

        """
        brep = conversions.brep_to_rhino(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            brep.Transform(transformation)

        return brep
