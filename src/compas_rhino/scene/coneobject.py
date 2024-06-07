from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import cone_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoConeObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing cone shapes."""

    def draw(self):
        """Draw the cone associated with the scene object.

        Returns
        -------
        System.Guid
            The GUID of the object created in Rhino.

        """
        attr = self.compile_attributes()
        geometry = cone_to_rhino_brep(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBrep(geometry, attr)]
        return self.guids
