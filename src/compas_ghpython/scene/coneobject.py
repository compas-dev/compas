from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class ConeObject(GHSceneObject, GeometryObject):
    """Scene object for drawing cone shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Cone`
        A COMPAS cone.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cone, **kwargs):
        super(ConeObject, self).__init__(geometry=cone, **kwargs)

    def draw(self):
        """Draw the cone associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino breps.

        """
        brep = conversions.cone_to_rhino_brep(self.geometry)
        transformation = conversions.transformation_to_rhino(self.transformation_world)
        brep.Transform(transformation)

        self._guids = [brep]
        return self.guids
