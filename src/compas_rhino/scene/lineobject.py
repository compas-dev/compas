from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoLineObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing lines."""

    def draw(self):
        """Draw the line.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        attr = self.compile_attributes()
        geometry = line_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddLine(geometry, attr)]
        return self.guids
