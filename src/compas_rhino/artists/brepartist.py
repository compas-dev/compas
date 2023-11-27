from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.colors import Color
from compas_rhino.conversions import brep_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas.artists import GeometryArtist
from .artist import RhinoArtist
from ._helpers import attributes


class BrepArtist(RhinoArtist, GeometryArtist):
    """An artist for drawing a RhinoBrep.

    Parameters
    ----------
    brep : :class:`compas_rhino.geometry.RhinoBrep`
        The Brep to draw.

    """

    def __init__(self, brep, **kwargs):
        super(BrepArtist, self).__init__(geometry=brep, **kwargs)

    def draw(self, color=None):
        """Bakes the Brep into the current document

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the Brep.

        Returns
        -------
        System.Guid
            The guid of the baked Brep.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = brep_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        return sc.doc.Objects.AddBrep(geometry, attr)
