from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas.geometry import Point

from .vector import RhinoVector


__all__ = ['RhinoPoint']


class RhinoPoint(RhinoVector):
    """Wrapper for Rhino points.

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

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a point wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Point3d` or :class:`Point` or list of float
            The input geometry.

        Returns
        -------
        :class:`RhinoPoint`
            The Rhino point wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Point3d):
            geometry = Rhino.Geometry.Point3d(geometry[0], geometry[1], geometry[2])
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
        :class:`RhinoPoint`
            The Rhino point wrapper.
        """
        guid = compas_rhino.select_point()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert the wrapper to a COMPAS point.

        Returns
        -------
        :class:`Point`
            A COMPAS point.
        """
        return Point(self.x, self.y, self.z)

    def closest_point(self, point, maxdist=0.0, return_param=False):
        """Compute the closest point to a point in space.

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
        tuple
            The XYZ coordinates of the point.

        """
        return self.xyz
