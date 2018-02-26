from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys

try:
    import PySide2
except ImportError:
    from PySide import QtCore
    from PySide import QtGui
    import PySide.QtGui as QtWidgets
else:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['App', ]


class App(QtWidgets.QApplication):
    """"""

    def __init__(self):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.setApplicationName("Viewer app")

    def start(self):
        sys.exit(self.exec_())


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
