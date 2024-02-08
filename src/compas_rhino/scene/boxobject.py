from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject


class RhinoBoxObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing box shapes.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, box, **kwargs):
        super(RhinoBoxObject, self).__init__(geometry=box, **kwargs)
        self.box = box

    def draw(self):
        """Draw the box associated with the scene object.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        geometry = box_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBox(geometry, attr)]
        return self.guids
