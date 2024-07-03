from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class CylinderObject(GHSceneObject, GeometryObject):
    """Scene object for drawing cylinder shapes."""

    def draw(self):
        """Draw the cylinder associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino breps.

        """
        geometry = conversions.cylinder_to_rhino_brep(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
