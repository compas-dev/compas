from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import torus_to_rhino_brep
from .artist import RhinoArtist
from ._helpers import attributes


class TorusArtist(RhinoArtist, GeometryArtist):
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

    def draw(self, color=None):
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the torus.

        Returns
        -------
        System.Guid
            The GUID of the object created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        brep = torus_to_rhino_brep(self.geometry)
        return sc.doc.Objects.AddBrep(brep, attr)
