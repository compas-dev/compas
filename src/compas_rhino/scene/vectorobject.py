from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.geometry import Point
from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class VectorObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing vectors.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`
        A COMPAS vector.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, vector, **kwargs):
        super(VectorObject, self).__init__(geometry=vector, **kwargs)

    def draw(self, color=None, point=None):
        """Draw the vector.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the vector.
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer, arrow="end")

        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.geometry
        start_geometry = point_to_rhino(start)
        end_geometry = point_to_rhino(end)
        if self.transformation:
            transformation = transformation_to_rhino(self.transformation)
            start_geometry.Transform(transformation)
            end_geometry.Transform(transformation)

        self._guids = [sc.doc.Objects.AddLine(start_geometry, end_geometry, attr)]
        return self.guids
