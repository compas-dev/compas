from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from ..conversions import point_to_rhino
from ..conversions import point_to_compas
from .vector import RhinoVector


class RhinoPoint(RhinoVector):
    """Wrapper for Rhino points.
    """

    def __init__(self):
        super(RhinoPoint, self).__init__()

    @classmethod
    def from_guid(cls, guid):
        """Construct a Rhino object wrapper from the GUID of an existing Rhino object.

        Parameters
        ----------
        guid : str
            The GUID of the Rhino object.

        Returns
        -------
        :class:`RhinoPoint`
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
            geometry = point_to_rhino(geometry)
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
            Default is ``False``.

        Returns
        -------
        tuple
            The XYZ coordinates of the point.

        """
        return self.geometry.X, self.geometry.Y, self.geometry.Z
