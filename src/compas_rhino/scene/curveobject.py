from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject


class RhinoCurveObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing curves.

    Parameters
    ----------
    curve : :class:`compas.geometry.Curve`
        A COMPAS curve.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, curve, **kwargs):
        super(RhinoCurveObject, self).__init__(geometry=curve, **kwargs)

    def draw(self):
        """Draw the curve.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        geometry = curve_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddCurve(geometry, attr)]
        return self.guids
