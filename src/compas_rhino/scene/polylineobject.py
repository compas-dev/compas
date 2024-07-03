from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import polyline_to_rhino
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoPolylineObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing polylines."""

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        geometry = polyline_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddPolyline(geometry, attr)]
        return self.guids
