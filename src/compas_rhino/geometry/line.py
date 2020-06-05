from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.geometry import Line
from compas_rhino.geometry._geometry import RhinoGeometry

if compas.IPY:
    import Rhino


__all__ = ['RhinoLine']


class RhinoLine(RhinoGeometry):
    """Convenience wrapper for a Rhino point object.

    Attributes
    ----------
    start : Rhino.Geometry.Point3d, read-only
        The starting point of the line.
    end : Rhino.Geometry.Point3d
        The end point of the line.
    """

    def __init__(self):
        super(RhinoLine, self).__init__()

    @property
    def start(self):
        return self.geometry.From

    @property
    def end(self):
        return self.geometry.To

    @classmethod
    def from_geometry(cls, geometry):
        if not isinstance(geometry, Rhino.Geometry.Line):
            start = Rhino.Geometry.Point3d(geometry[0][0], geometry[0][1], geometry[0][2])
            end = Rhino.Geometry.Point3d(geometry[1][0], geometry[1][1], geometry[1][2])
            geometry = Rhino.Geometry.Line(start, end)
        line = cls()
        line.geometry = geometry
        return line

    def to_compas(self):
        return Line(self.start, self.end)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    line = RhinoLine.from_geometry(Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]))

    print(line.guid)
    print(line.object)
    print(line.geometry)
    print(line.type)
    print(line.name)

    print(line.start)
    print(line.end)

    print(line.to_compas())
