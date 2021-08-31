from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
import compas_rhino
from compas.geometry import Vector

from ._geometry import BaseRhinoGeometry


__all__ = ['RhinoVector']


class RhinoVector(BaseRhinoGeometry):
    """Wrapper for Rhino vectors.

    Attributes
    ----------
    x (read-only) : float
        The X coordinate.
    y (read-only) : float
        The Y coordinate.
    z (read-only) : float
        The Z coordinate.
    xyz (read-only) : list
        The XYZ coordinates.

    """

    def __init__(self):
        super(RhinoVector, self).__init__()

    @property
    def x(self):
        return self.geometry.X

    @property
    def y(self):
        return self.geometry.Y

    @property
    def z(self):
        return self.geometry.Z

    @property
    def xyz(self):
        return (self.x, self.y, self.z)

    @classmethod
    def from_guid(cls, guid):
        """Construct a Rhino object wrapper from the GUID of an existing Rhino object.

        Parameters
        ----------
        guid : str
            The GUID of the Rhino object.

        Returns
        -------
        :class:`RhinoVector`
            The Rhino vector wrapper.
        """
        obj = compas_rhino.find_object(guid)
        wrapper = cls()
        wrapper.guid = obj.Id
        wrapper.object = obj
        wrapper.geometry = obj.Geometry.Location
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a vector wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Vector3d` or :class:`Vector` or list of float
            The input geometry.

        Returns
        -------
        :class:`RhinoVector`
            The Rhino vector wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Vector3d):
            geometry = Rhino.Geometry.Vector3d(geometry[0], geometry[1], geometry[2])
        vector = cls()
        vector.geometry = geometry
        return vector

    def to_compas(self):
        """Convert the wrapper to a COMPAS object.

        Returns
        -------
        :class:`Vector`
            A COMPAS vector.
        """
        return Vector(self.x, self.y, self.z)
