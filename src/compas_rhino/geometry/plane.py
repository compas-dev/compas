from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Plane
from compas.geometry import Frame

from ._geometry import BaseRhinoGeometry


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
        geometry : tuple of point and normal or :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Plane` or :class:`compas.geometry.Frame`
            The geometry object defining a plane.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoPlane`
            The wrapped plane.
        """
        if not isinstance(geometry, Rhino.Geometry.Plane):
            if isinstance(geometry, Plane):
                point = Rhino.Geometry.Point3d(geometry[0][0], geometry[0][1], geometry[0][2])
                normal = Rhino.Geometry.Vector3d(geometry[1][0], geometry[1][1], geometry[1][2])
                geometry = Rhino.Geometry.Plane(point, normal)
            elif isinstance(geometry, Frame):
                point = Rhino.Geometry.Point3d(geometry[0][0], geometry[0][1], geometry[0][2])
                xaxis = Rhino.Geometry.Vector3d(geometry[1][0], geometry[1][1], geometry[1][2])
                yaxis = Rhino.Geometry.Vector3d(geometry[2][0], geometry[2][1], geometry[2][2])
                geometry = Rhino.Geometry.Plane(point, xaxis, yaxis)
            else:
                point = Rhino.Geometry.Point3d(geometry[0][0], geometry[0][1], geometry[0][2])
                normal = Rhino.Geometry.Vector3d(geometry[1][0], geometry[1][1], geometry[1][2])
                geometry = Rhino.Geometry.Plane(point, normal)
        line = cls()
        line.geometry = geometry
        return line

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Frame`
            A COMPAS frame object.
        """
        return Frame(self.point, self.xaxis, self.yaxis)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
