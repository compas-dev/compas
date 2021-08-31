from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Frame

from compas_rhino.geometry._geometry import BaseRhinoGeometry


__all__ = ['RhinoPlane']


class RhinoPlane(BaseRhinoGeometry):
    """Wrapper for a Rhino plane objects.

    Attributes
    ----------
    point (read-only) : :class:`Rhino.Geometry.Point3d`
        Base point of the plane.
    normal (read-only) : :class:`Rhino.Geometry.Vector3d`
        The normal vector of the plane.
    xaxis (read-only) : :class:`Rhino.Geometry.Vector3d`
        The X axis of the plane.
    yaxis (read-only) : :class:`Rhino.Geometry.Vector3d`
        The Y axis of the plane.

    Notes
    -----
    In Rhino, a plane and a frame are equivalent.
    Therefore, the COMPAS conversion function of this class returns a frame object instead of a plane.

    """

    def __init__(self):
        super(RhinoPlane, self).__init__()

    @property
    def point(self):
        return self.geometry.Origin

    @property
    def normal(self):
        return self.geometry.Normal

    @property
    def xaxis(self):
        return self.geometry.XAxis

    @property
    def yaxis(self):
        return self.geometry.YAxis

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a plane wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Plane` or :class:`compas.geometry.Frame` or tuple of point and normal
            The geometry object defining a plane.

        Returns
        -------
        :class:`RhinoPlane`
            The Rhino plane wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Plane):
            if isinstance(geometry, Frame):
                point, xaxis, yaxis = geometry
                point = Rhino.Geometry.Point3d(point[0], point[1], point[2])
                xaxis = Rhino.Geometry.Vector3d(xaxis[0], xaxis[1], xaxis[2])
                yaxis = Rhino.Geometry.Vector3d(yaxis[0], yaxis[1], yaxis[2])
                geometry = Rhino.Geometry.Plane(point, xaxis, yaxis)

            else:
                point, normal = geometry
                point = Rhino.Geometry.Point3d(point[0], point[1], point[2])
                normal = Rhino.Geometry.Vector3d(normal[0], normal[1], normal[2])
                geometry = Rhino.Geometry.Plane(point, normal)

        plane = cls()
        plane.geometry = geometry
        return plane

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`Frame`
            A COMPAS frame.
        """
        return Frame(self.point, self.xaxis, self.yaxis)
