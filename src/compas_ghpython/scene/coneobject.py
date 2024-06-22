from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class ConeObject(GHSceneObject, GeometryObject):
    """Scene object for drawing cone shapes."""

    def draw(self):
        """Draw the cone associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino breps.

        """
        brep = conversions.cone_to_rhino_brep(self.geometry)
        transformation = conversions.transformation_to_rhino(self.worldtransformation)
        brep.Transform(transformation)

        self._guids = [brep]
        return self.guids
