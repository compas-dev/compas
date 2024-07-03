from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import capsule_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoCapsuleObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing capsule shapes."""

    def draw(self):
        """Draw the capsule associated with the scene object.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        breps = capsule_to_rhino_brep(self.geometry)
        transformation = transformation_to_rhino(self.worldtransformation)
        for geometry in breps:
            geometry.Transform(transformation)

        self._guids = [sc.doc.Objects.AddBrep(brep, attr) for brep in breps]
        return self.guids
