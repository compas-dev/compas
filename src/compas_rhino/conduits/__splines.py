from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line

    from System.Collections.Generic import List
    from System.Drawing.colour import FromArgb

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['SplinesConduit', ]


class SplinesConduit(Conduit):
    """"""
    def __init__(self, points, lines, splines,
                 thickness=1,
                 spline_thickness=5,
                 colour=None,
                 spline_colour=None,
                 **kwargs):

        super(SplinesConduit, self).__init__(**kwargs)
        self.points = points
        self.lines = lines
        self.splines = splines
        self.lines_count = len(lines)
        self.thickness = thickness
        self.spline_thickness = spline_thickness
        colour = colour or (255, 0, 0)
        spline_colour = spline_colour or (0, 0, 255)
        self.colour = FromArgb(*colour)
        self.spline_colour = FromArgb(*spline_colour)

    def DrawForeground(self, e):

        lines = List[Line](self.lines_count)
        for i, j in self.lines:
            sp = self.points[i]
            ep = self.points[j]
            lines.Add(Line(Point3d(*sp), Point3d(*ep)))
        e.Display.DrawLines(lines, self.colour, self.thickness)
        for i, (u, v) in enumerate(self.splines):
            sp = self.points[u]
            ep = self.points[v]
            th = self.spline_thickness[i]
            e.Display.DrawLine(Line(Point3d(*sp), Point3d(*ep)), self.spline_colour, th)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    points    = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(10)]
    lines     = [(i, i + 1) for i in range(0, 4)]
    splines   = [(i, i + 1) for i in range(5, 9)]
    thickness = [2 * i for i in range(len(splines))]

    try:
        conduit = SplinesConduit(points, lines, splines, thickness=1, spline_thickness=thickness)
        conduit.Enabled = True

        for i in range(100):
            conduit.points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(10)]

            conduit.redraw()

            time.sleep(0.1)

    except Exception as e:
        print(e)

    finally:
        conduit.Enabled = False
        del conduit
