from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Frame

from compas_rhino.geometry._geometry import BaseRhinoGeometry


__all__ = ['RhinoEllipse']


class RhinoEllipse(BaseRhinoGeometry):
    """Wrapper for a Rhino ellipse objects.

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
        super(RhinoEllipse, self).__init__()

    @property
    def plane(self):
        return self.geometry.Plane

    @property
    def radius(self):
        return self.geometry.Radius

    @property
    def center(self):
        return self.geometry.Center

    @property
    def normal(self):
        return self.geometry.Normal

    @classmethod
    def from_geometry(cls, geometry):
        """Construct an ellipse wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Ellipse` or :class:`compas.geometry.Ellipse` or tuple of plane and major and minor
            The geometry object defining an ellipse.

        Returns
        -------
        :class:`RhinoEllipse`
            The Rhino ellipse wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Ellipse):
            plane, radius = geometry
            point, normal = plane
            point = Rhino.Geometry.Point3d(point[0], point[1], point[2])
            normal = Rhino.Geometry.Vector3d(normal[0], normal[1], normal[2])
            plane = Rhino.Geometry.Plane(point, normal)
            geometry = Rhino.Geometry.Ellipse(plane, radius)

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
        :class:`Ellipse`
            A COMPAS ellipse.
        """
        return Frame(self.point, self.xaxis, self.yaxis)
