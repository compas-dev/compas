from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import torus_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoTorusObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing torus shapes."""

    def draw(self):
        """Draw the torus associated with the scene object.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        brep = torus_to_rhino_brep(self.geometry)
        brep.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBrep(brep, attr)]
        return self.guids
