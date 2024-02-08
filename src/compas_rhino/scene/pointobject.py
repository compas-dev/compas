from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from .helpers import attributes


class PointObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing points.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, point, **kwargs):
        super(PointObject, self).__init__(geometry=point, **kwargs)

    def draw(self):
        """Draw the point.

        Returns
        -------
        list[System.Guid]
            List of GUIDs of the objects created in Rhino.

        """
        attr = attributes(name=self.geometry.name, color=self.color, layer=self.layer)
        geometry = point_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddPoint(geometry, attr)]
        return self.guids
