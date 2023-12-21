from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class LineObject(GHSceneObject, GeometryObject):
    """Scene object for drawing lines.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, line, **kwargs):
        super(LineObject, self).__init__(geometry=line, **kwargs)

    def draw(self):
        """Draw the line.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]
            List of created Rhino lines.

        """
        geometry = conversions.line_to_rhino(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.transformation_world))

        self._guids = [geometry]
        return self.guids
