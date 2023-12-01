from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class PointObject(GHSceneObject, GeometryObject):
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
        :rhino:`Rhino.Geometry.Point3d`

        """
        geometry = conversions.point_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        return geometry
