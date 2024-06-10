from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class LineObject(GHSceneObject, GeometryObject):
    """Scene object for drawing lines."""

    def draw(self):
        """Draw the line.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]
            List of created Rhino lines.

        """
        geometry = conversions.line_to_rhino(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
