from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import capsule_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


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

    def draw(self, color=None):
        """Draw the capsule associated with the scene object.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the capsule.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        breps = capsule_to_rhino_brep(self.geometry)
        transformation = transformation_to_rhino(self.transformation_world)
        for geometry in breps:
            geometry.Transform(transformation)

        self._guids = [sc.doc.Objects.AddBrep(brep, attr) for brep in breps]
        return self.guids
