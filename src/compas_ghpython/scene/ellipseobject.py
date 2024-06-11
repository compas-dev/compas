from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class EllipseObject(GHSceneObject, GeometryObject):
    """Scene object for drawing ellipses."""

    def draw(self):
        """Draw the ellipse.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Ellipse`]
            List of created Rhino ellipse.

        """
        ellipse = conversions.ellipse_to_rhino(self.geometry)
        ellipse = ellipse.ToNurbsCurve()
        ellipse.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [ellipse]
        return self.guids
