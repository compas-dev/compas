from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class TorusObject(GHSceneObject, GeometryObject):
    """Scene object for drawing torus shapes."""

    def draw(self):
        """Draw the torus associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino torus.

        """
        brep = conversions.torus_to_rhino_brep(self.geometry)
        brep.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [brep]
        return self.guids
