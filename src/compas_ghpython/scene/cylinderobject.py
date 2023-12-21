from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class CylinderObject(GHSceneObject, GeometryObject):
    """Scene object for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cylinder, **kwargs):
        super(CylinderObject, self).__init__(geometry=cylinder, **kwargs)

    def draw(self):
        """Draw the cylinder associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino breps.
        """
        geometry = conversions.cylinder_to_rhino_brep(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.transformation_world))

        self._guids = [geometry]
        return self.guids
