from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from compas.viewers.core import Camera
from compas.viewers.core import Mouse
from compas.viewers.core import Grid
from compas.viewers.core import Axes
from compas.viewers.core import GLWidget
from compas.viewers.core import Controller
from compas.viewers.core import App


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Viewer', ]


class Front(Controller):
    """"""

    settings = {}


class View(GLWidget):
    """"""

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller

    @property
    def settings(self):
        return self.controller.settings

    def paint(self):
        pass


class Viewer(App):
    """"""

    def __init__(self, config=None, style=None):
        super(Viewer, self).__init__(config, style)
        self.config = config
        self.controller = Front(self)
        self.view = View(self.controller)
        self.setup()
        self.init()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    config = {
        # 'menubar': [
        # ],
        # 'toolbar': [
        # ],
        # 'sidebar': [
        # ],
        # 'console': [
        # ] 
    }

    viewer = Viewer(config)
    viewer.show()
