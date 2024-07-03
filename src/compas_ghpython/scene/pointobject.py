from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class PointObject(GHSceneObject, GeometryObject):
    """Scene object for drawing points."""

    def draw(self):
        """Draw the point.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]
            List of created Rhino points.
        """
        geometry = conversions.point_to_rhino(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
