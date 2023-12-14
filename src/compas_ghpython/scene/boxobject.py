from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class BoxObject(GHSceneObject, GeometryObject):
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

    def draw(self):
        """Draw the box associated with the scene object.

        Returns
        -------
        :rhino:`Rhino.Geometry.Box`

        """
        box = conversions.box_to_rhino(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            box.Transform(transformation)

        self._guids = [box]
        return self._guids
