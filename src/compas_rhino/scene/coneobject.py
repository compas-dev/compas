from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import cone_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from .helpers import attributes


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

    def draw(self):
        """Draw the cone associated with the scene object.

        Returns
        -------
        System.Guid
            The GUID of the object created in Rhino.

        """
        attr = attributes(name=self.geometry.name, color=self.color, layer=self.layer)
        geometry = cone_to_rhino_brep(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBrep(geometry, attr)]
        return self.guids
