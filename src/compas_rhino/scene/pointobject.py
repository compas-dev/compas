from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class PointObject(RhinoSceneObject, GeometryObject):
    """Sceneobject for drawing points.

    Parameters
    ----------
    point : :class:`~compas.geometry.Point`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, point, **kwargs):
        super(PointObject, self).__init__(geometry=point, **kwargs)

    def draw(self, color=None):
        """Draw the point.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the point.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        geometry = point_to_rhino(self.geometry)
        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))
        return sc.doc.Objects.AddPoint(geometry, attr)
