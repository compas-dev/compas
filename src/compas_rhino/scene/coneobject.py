from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import cone_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class ConeObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing cone shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Cone`
        A COMPAS cone.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cone, **kwargs):
        super(ConeObject, self).__init__(geometry=cone, **kwargs)

    def draw(self, color=None):
        """Draw the cone associated with the scene object.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the cone.

        Returns
        -------
        System.Guid
            The GUID of the object created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = cone_to_rhino_brep(self.geometry)

        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        self._guids = [sc.doc.Objects.AddBrep(geometry, attr)]
        return self.guids
