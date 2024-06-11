from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Point
from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class VectorObject(GHSceneObject, GeometryObject):
    """Scene object for drawing vectors."""

    def draw(self, point=None):
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]
            List of created Rhino lines.

        """
        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.geometry

        geometry = conversions.line_to_rhino([start, end])
        transformation = conversions.transformation_to_rhino(self.worldtransformation)
        geometry.Transform(transformation)

        self._guids = [geometry]
        return self.guids
