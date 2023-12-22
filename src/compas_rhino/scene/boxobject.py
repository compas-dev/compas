from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class BoxObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing box shapes.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, box, **kwargs):
        super(BoxObject, self).__init__(geometry=box, **kwargs)
        self.box = box

    def draw(self, color=None):
        """Draw the box associated with the scene object.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the box.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = box_to_rhino(self.geometry)
        transformation = transformation_to_rhino(self.worldtransformation)
        geometry.Transform(transformation)

        self._guids = [sc.doc.Objects.AddBox(geometry, attr)]
        return self.guids
