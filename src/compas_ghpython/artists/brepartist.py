from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino.conversions import brep_to_rhino
from .artist import GHArtist


class BrepArtist(GHArtist):
    """An artist for drawing a brep in Grasshopper.

    Parameters
    ----------
    brep : :class:`~compas_rhino.geometry.RhinoBrep`
        The brep to draw.

    """

    def __init__(self, brep, **kwargs):
        super(BrepArtist, self).__init__(**kwargs)
        self._brep = brep

    def draw(self):
        """Draw the brep as a Grasshopper geometry.

        Returns
        -------
        :rhino:`Rhino.Geometry.Brep`
            The Grasshopper geometry instance.

        """
        return brep_to_rhino(self._brep)
