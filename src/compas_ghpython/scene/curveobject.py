from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class CurveObject(GHSceneObject, GeometryObject):
    """Scene object for drawing curves.

    Parameters
    ----------
    curve : :class:`compas.geometry.Curve`
        A COMPAS curve.

    Other Parameters
    ----------------
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, curve, **kwargs):
        super(CurveObject, self).__init__(geometry=curve, **kwargs)

    def draw(self):
        """Draw the curve.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Curve`]

        """
        geometry = conversions.curve_to_rhino(self.geometry)
        transformation = conversions.transformation_to_rhino(self.worldtransformation)
        geometry.Transform(transformation)

        self._guids = [geometry]
        return self.guids
