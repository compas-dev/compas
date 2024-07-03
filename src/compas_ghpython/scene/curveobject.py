from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class CurveObject(GHSceneObject, GeometryObject):
    """Scene object for drawing curves."""

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
