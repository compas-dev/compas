from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class SphereObject(GHSceneObject, GeometryObject):
    """Scene object for drawing sphere shapes."""

    def draw(self):
        """Draw the sphere associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Sphere`]
            List of created Rhino spheres.

        """
        geometry = conversions.sphere_to_rhino(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
