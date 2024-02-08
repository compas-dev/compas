from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas_rhino.conversions import brep_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas.scene import GeometryObject
from .sceneobject import RhinoSceneObject
from .helpers import attributes


class BrepObject(RhinoSceneObject, GeometryObject):
    """A scene object for drawing a RhinoBrep.

    Parameters
    ----------
    brep : :class:`compas_rhino.geometry.RhinoBrep`
        The Brep to draw.

    """

    def __init__(self, brep, **kwargs):
        super(BrepObject, self).__init__(geometry=brep, **kwargs)

    def draw(self):
        """Bakes the Brep into the current document

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = attributes(name=self.geometry.name, color=self.color, layer=self.layer)
        geometry = brep_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBrep(geometry, attr)]
        return self.guids
