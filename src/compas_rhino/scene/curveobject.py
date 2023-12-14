from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class CurveObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing curves.

    Parameters
    ----------
    curve : :class:`compas.geometry.Curve`
        A COMPAS curve.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, curve, **kwargs):
        super(CurveObject, self).__init__(geometry=curve, **kwargs)

    def draw(self, color=None):
        """Draw the curve.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the curve.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the object created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = curve_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        self._guids = [sc.doc.Objects.AddCurve(geometry, attr)]
        return self.guids
