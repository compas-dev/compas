from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class CurveArtist(RhinoArtist, GeometryObject):
    """Artist for drawing curves.

    Parameters
    ----------
    curve : :class:`~compas.geometry.Curve`
        A COMPAS curve.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, curve, **kwargs):
        super(CurveArtist, self).__init__(geometry=curve, **kwargs)

    def draw(self, color=None):
        """Draw the curve.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the curve.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = curve_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        return sc.doc.Objects.AddCurve(geometry, attr)
