from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from PySide.QtCore import QPoint


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['Mouse', ]


class Mouse(object):
    """"""
    def __init__(self, view):
        self.view  = view
        self.pos = QPoint()
        self.last_pos = QPoint()

    def dx(self):
        return self.pos.x() - self.last_pos.x()

    def dy(self):
        return self.pos.y() - self.last_pos.y()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
