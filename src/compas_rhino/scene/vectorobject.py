from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.geometry import Point
from compas.scene import GeometryObject
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoVectorObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing vectors."""

    def draw(self):
        """Draw the vector.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes(arrow="end")
        start = Point(0, 0, 0)
        end = start + self.geometry
        start_geometry = point_to_rhino(start)
        end_geometry = point_to_rhino(end)
        transformation = transformation_to_rhino(self.worldtransformation)
        start_geometry.Transform(transformation)
        end_geometry.Transform(transformation)

        self._guids = [sc.doc.Objects.AddLine(start_geometry, end_geometry, attr)]
        return self.guids
