from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys

from functools import partial

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


__all__ = ['Sidebar']


class Sidebar(QtWidgets.QDockWidget):
    pass



# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
