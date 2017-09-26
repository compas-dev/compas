from __future__ import print_function

from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['PointPairsConduit', ]


class PointPairsConduit(Conduit):
    """"""
    def __init__(self, points, pairs, thickness=1, color=None, **kwargs):
        super(PointPairsConduit, self).__init__(**kwargs)
        self.points = points
        self.pairs = pairs
        self.n = len(pairs)
        self.thickness = thickness
        color = color or (255, 255, 255)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        lines = List[Line](self.n)
        for i, j in self.pairs:
            start = self.points[i]
            end = self.points[j]
            lines.Add(Line(Point3d(*start), Point3d(*end)))
        e.Display.DrawLines(lines, self.color, self.thickness)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
    pairs  = [(i, i + 1) for i in range(99)]

    try:
        conduit = PointPairsConduit(points, pairs)
        conduit.Enabled = True

        for i in range(100):
            conduit.points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]

            conduit.redraw()

            time.sleep(0.1)

    except Exception as e:
        print(e)

    finally:
        conduit.Enabled = False
        del conduit
