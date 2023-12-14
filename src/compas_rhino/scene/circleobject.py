from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import circle_to_rhino

# from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class CircleObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing circles.

    Parameters
    ----------
    circle : :class:`compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, circle, **kwargs):
        super(CircleObject, self).__init__(geometry=circle, **kwargs)

    def draw(self, color=None):
        """Draw the circle.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the circle.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the object created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = circle_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        self._guids = [sc.doc.Objects.AddCircle(geometry, attr)]
        return self.guids
