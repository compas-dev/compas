from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from ._primitives import point_to_rhino
from ._primitives import point_to_compas

from .vector import RhinoVector


class RhinoPoint(RhinoVector):
    """Wrapper for Rhino points."""

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, obj):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        obj : :rhino:`Rhino_DocObjects_PointObject`
            The input object.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a point.

        """
        self._guid = obj.Id
        self._object = obj
        self.geometry = obj.Geometry.Location

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Point3d` | :class:`~compas.geometry.Point` or list of float
            The input geometry.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a plane.

        """
        if not isinstance(geometry, Rhino.Geometry.Point3d):
            geometry = point_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert the wrapper to a COMPAS point.

        Returns
        -------
        :class:`~compas.geometry.Point`
            A COMPAS point.
        """
        return point_to_compas(self.geometry)

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
            Default is False.

        Returns
        -------
        tuple
            The XYZ coordinates of the point.

        """
        return self.geometry.X, self.geometry.Y, self.geometry.Z
