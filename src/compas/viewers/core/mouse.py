from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    import PySide2
except ImportError:
    from PySide import QtCore
else:
    from PySide2 import QtCore


__all__ = ['Mouse']


class Mouse(object):
    """"""

    def __init__(self, view):
        self.view  = view
        self.pos = QtCore.QPoint()
        self.last_pos = QtCore.QPoint()

    def dx(self):
        return self.pos.x() - self.last_pos.x()

    def dy(self):
        return self.pos.y() - self.last_pos.y()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
