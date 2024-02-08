from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import capsule_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from .helpers import attributes


class CapsuleObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing capsule shapes.

    Parameters
    ----------
    capsule : :class:`compas.geometry.Capsule`
        A COMPAS capsule.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, capsule, **kwargs):
        super(CapsuleObject, self).__init__(geometry=capsule, **kwargs)

    def draw(self):
        """Draw the capsule associated with the scene object.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = attributes(name=self.geometry.name, color=self.color, layer=self.layer)
        breps = capsule_to_rhino_brep(self.geometry)
        transformation = transformation_to_rhino(self.worldtransformation)
        for geometry in breps:
            geometry.Transform(transformation)

        self._guids = [sc.doc.Objects.AddBrep(brep, attr) for brep in breps]
        return self.guids
