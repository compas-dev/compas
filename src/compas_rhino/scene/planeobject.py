from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.scene import GeometryObject
from .sceneobject import RhinoSceneObject


class PlaneObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing planes.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane`
        A COMPAS plane.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, plane, **kwargs):
        super(PlaneObject, self).__init__(geometry=plane, **kwargs)

    def draw(self):
        """Draw the plane.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        raise NotImplementedError
