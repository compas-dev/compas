from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import curve_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class CurveArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing curves.

    Parameters
    ----------
    curve : :class:`~compas.geometry.Curve`
        A COMPAS curve.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`~compas.artists.GeometryArtist`.

    """

    def __init__(self, curve, **kwargs):
        super(CurveArtist, self).__init__(geometry=curve, **kwargs)

    def draw(self, color=None):
        """Draw the curve.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.
            The default color is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        guid = sc.doc.Objects.AddCurve(curve_to_rhino(self.geometry), attr)
        return [guid]
