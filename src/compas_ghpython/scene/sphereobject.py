from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class SphereObject(GHSceneObject, GeometryObject):
    """Scene object for drawing sphere shapes.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`
        A COMPAS sphere.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, sphere, **kwargs):
        super(SphereObject, self).__init__(geometry=sphere, **kwargs)

    def draw(self):
        """Draw the sphere associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Sphere`]
            List of created Rhino spheres.

        """
        geometry = conversions.sphere_to_rhino(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.transformation_world))

        self._guids = [geometry]
        return self.guids
