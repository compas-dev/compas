from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import cylinder_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject


class RhinoCylinderObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cylinder, **kwargs):
        super(RhinoCylinderObject, self).__init__(geometry=cylinder, **kwargs)

    def draw(self):
        """Draw the cylinder associated with the scene object.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        geometry = cylinder_to_rhino_brep(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBrep(geometry, attr)]
        return self.guids
