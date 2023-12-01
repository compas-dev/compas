from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino import conversions

from compas.geometry import Point
from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class VectorObject(GHSceneObject, GeometryObject):
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

    def draw(self, point=None, show_point=False):
        """Draw the vector.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

        Returns
        -------
        :rhino:`Rhino.Geometry.Line`

        """
        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.geometry

        geometry = conversions.line_to_rhino([start, end])

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            geometry.Transform(transformation)

        return geometry
