from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# TODO: this should have a base brep artist
# TODO: brep drawing should be handled here

import compas_rhino
from .artist import RhinoArtist


class BrepArtist(RhinoArtist):
    """An artist for drawing a RhinoBrep.

    Parameters
    ----------
    brep : :class:`~compas_rhino.geometry.RhinoBrep`
        The Brep to draw.

    """

    def __init__(self, brep, **kwargs):
        super(BrepArtist, self).__init__(**kwargs)
        self._brep = brep

    def draw(self, color=None):
        """Bakes the Brep into the current document

        Returns
        -------
        list(:rhino:`System.Guid`)
            The guid of the baked Brep.

        """
        return [compas_rhino.draw_brep(self._brep, color)]
