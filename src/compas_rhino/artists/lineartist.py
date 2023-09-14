from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import line_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class LineArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing lines.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, line, **kwargs):
        super(LineArtist, self).__init__(geometry=line, **kwargs)

    def draw(self, color=None):
        """Draw the line.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the line.
            Default is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = line_to_rhino(self.geometry)

        return sc.doc.Objects.AddLine(geometry, attr)
