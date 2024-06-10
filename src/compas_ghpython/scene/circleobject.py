from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class CircleObject(GHSceneObject, GeometryObject):
    """Scene object for drawing circles."""

    def draw(self):
        """Draw the circle.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Circle`]
            List of created Rhino circles.

        """
        circle = conversions.circle_to_rhino(self.geometry)
        transformation = conversions.transformation_to_rhino(self.worldtransformation)
        circle.Transform(transformation)

        self._guids = [circle]
        return self.guids
