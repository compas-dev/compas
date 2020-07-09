from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.geometry import Plane
from compas.geometry import Frame
from compas_rhino.geometry import RhinoGeometry

if compas.IPY:
    import Rhino


__all__ = ['RhinoPlane']


class RhinoPlane(RhinoGeometry):
    """Convenience wrapper for a Rhino point object."""

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

    def to_compas(self):
        return Frame(self.point, self.xaxis, self.yaxis)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    plane = RhinoPlane.from_geometry(Plane([0, 0, 0], [0, 0, 1]))

    print(plane.guid)
    print(plane.object)
    print(plane.geometry)
    print(plane.type)
    print(plane.name)

    print(plane.point)
    print(plane.normal)

    print(plane.xaxis)
    print(plane.yaxis)

    print(plane.to_compas())
