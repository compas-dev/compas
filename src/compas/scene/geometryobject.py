from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .sceneobject import SceneObject


class GeometryObject(SceneObject):
    """Base class for scene objects for geometry objects.

    Parameters
    ----------
    geometry : :class:`compas.geometry.Geometry`
        The geometry of the geometry.

    Attributes
    ----------
    geometry : :class:`compas.geometry.Geometry`
        The geometry object associated with the scene object.
    color : :class:`compas.colors.Color`
        The color of the object.

    """

    def __init__(self, geometry, **kwargs):
        super(GeometryObject, self).__init__(item=geometry, **kwargs)
        self.geometry = geometry
