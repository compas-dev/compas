from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import Rhino.UI


__all__ = ['Mouse']


class Mouse(Rhino.UI.MouseCallback):
    """"""

    def __init__(self, parent=None):
        super(Mouse, self).__init__()
        self.parent = parent
        self.x = None  # x-coordinate of 2D point in the viewport
        self.y = None  # y-coordinate of 2D point in the viewport
        self.p1 = None  # start of the frustum line in world coordinates
        self.p2 = None  # end of the frustum line in world coordinates

    def OnMouseMove(self, e):
        line = e.View.ActiveViewport.ClientToWorld(e.ViewportPoint)
        self.x = e.ViewportPoint.X
        self.y = e.ViewportPoint.Y
        self.p1 = line.From
        self.p2 = line.To
        e.View.Redraw()

    def OnMouseDown(self, e):
        pass

    def OnMouseUp(self, e):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
