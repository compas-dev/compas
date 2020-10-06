from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas.geometry import Point

from ._geometry import BaseRhinoGeometry


__all__ = ['RhinoPoint']


class RhinoPoint(BaseRhinoGeometry):
    """Wrapper for Rhino point objects.

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
        super(RhinoPoint, self).__init__()

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
        return [self.x, self.y, self.z]

    @classmethod
    def from_guid(cls, guid):
        """Construct a Rhino object wrapper from the GUID of an existing Rhino object.

        Parameters
        ----------
        guid : str
            The GUID of the Rhino object.

        Returns
        -------
        :class:`compas_rhino.geometry.BaseRhinoGeometry`
            The Rhino object wrapper.
        """
        obj = compas_rhino.find_object(guid)
        wrapper = cls()
        wrapper.guid = obj.Id
        wrapper.object = obj
        wrapper.geometry = obj.Geometry.Location
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a point wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : point or :class:`Rhino.Geometry.Point3d`
            The input geometry.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoPoint`
            The wrapped point.
        """
        if not isinstance(geometry, Rhino.Geometry.Point3d):
            geometry = Rhino.Geometry.Point3d(* geometry)
        point = cls()
        point.geometry = geometry
        return point

    @classmethod
    def from_selection(cls):
        """Construct as point wrapper from a selected point object.

        Parameters
        ----------
        None

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoPoint`
            The wrapped point.
        """
        guid = compas_rhino.select_point()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert the wrapper to a COMPAS point.

        Returns
        -------
        :class:`compas.geometry.Point`
            A COMPAS point.
        """
        return Point(self.x, self.y, self.z)

    def closest_point(self, point, maxdist=0.0, return_param=False):
        """Compute the closest point on a curve to a point in space.

        Parameters
        ----------
        point : point
            A point location.
        maxdist : float, optional
            The maximum distance between the point on the curve and the curve.
            Default is ``0.0``.
        return_param : bool, optional
            Return not only the point coordinates, but also the parameter of the point on the curve.
            Default is ``False``.

        Returns
        -------
        list
            The XYZ coordinates of the point.

        """
        return self.xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import Translation
    from compas.geometry import Rotation

    point = RhinoPoint.from_selection()
    # point = RhinoPoint.from_geometry(Point3d(0, 0, 0))
    # point = RhinoPoint.from_geometry(Point(0, 0, 0))

    print(point.guid)
    print(point.object)
    print(point.geometry)
    print(point.type)
    print(point.name)

    print(point.xyz)

    p = point.to_compas()

    print(p)

    T = Translation([1.0, 1.0, 0.0])
    R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], 0.5 * 3.14159)
    X = R * T

    point.transform(X)

    p = point.to_compas()

    print(p)
