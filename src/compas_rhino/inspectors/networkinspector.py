from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas_rhino.ui import Mouse

try:
    from System.Drawing import Color

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['NetworkInspector']


class NetworkInspector(object):

    def __init__(self, network, tol=0.1):
        super(NetworkInspector, self).__init__()
        self.mouse     = Mouse()
        self.network   = network
        self.tol       = tol
        self.dotcolor  = Color.FromArgb(255, 0, 0)
        self.textcolor = Color.FromArgb(0, 0, 0)

    # def DrawForeground(self, e):
    #     p1  = self.mouse.p1
    #     p2  = self.mouse.p2
    #     for i, p0 in enumerate(self.points):
    #         if distance_point_line(p0, (p1, p2)) < self.tol:
    #             e.Display.DrawDot(Point3d(*p0), str(i), self.dotcolor, self.textcolor)
    #             break

    def inspect_vertex(self, key):
        pass

    def inspect_edge(self, key):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
