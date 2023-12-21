from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import cylinder_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class CylinderObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cylinder, **kwargs):
        super(CylinderObject, self).__init__(geometry=cylinder, **kwargs)

    def draw(self, color=None):
        """Draw the cylinder associated with the scene object.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the cylinder.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = cylinder_to_rhino_brep(self.geometry)
        geometry.Transform(transformation_to_rhino(self.transformation_world))

        self._guids = [sc.doc.Objects.AddBrep(geometry, attr)]
        return self.guids
