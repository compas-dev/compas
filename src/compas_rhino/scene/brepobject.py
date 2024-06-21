from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import brep_to_rhino
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoBrepObject(RhinoSceneObject, GeometryObject):
    """A scene object for drawing a RhinoBrep."""

    def draw(self):
        """Bakes the Brep into the current document

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        geometry = brep_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBrep(geometry, attr)]
        return self.guids
