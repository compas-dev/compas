from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import surface_to_rhino
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoSurfaceObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing surfaces."""

    def draw(self):
        """Draw the surface.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        surface = surface_to_rhino(self.geometry)
        surface.Transform(transformation_to_rhino(self.worldtransformation))
        self._guids = [sc.doc.Objects.AddSurface(surface, attr)]
        return self.guids
