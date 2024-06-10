from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class PolylineObject(GHSceneObject, GeometryObject):
    """Scene object for drawing polylines."""

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.PolylineCurve`]
            List of created Rhino polyline.

        """
        geometry = conversions.polyline_to_rhino_curve(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
