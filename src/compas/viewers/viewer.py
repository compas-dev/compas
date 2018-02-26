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
from compas.viewers.core import GLView
from compas.viewers.core import Controller
from compas.viewers.core import App


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Viewer', ]


class Front(Controller):
    """"""

    def __init__(self):
        pass

    def test(self):
        print('test')


class View(GLView):
    """"""

    def __init__(self):
        super(View, self).__init__()

    def paint(self):
        pass


class Viewer(App):
    """"""

    def __init__(self, width=1440, height=900):
        super(Viewer, self).__init__()
        self.controller = Front()
        self.setup(width, height)
        self.init()
        self.show()

    def show(self):
        self.statusbar.showMessage('Ready')
        self.main.show()
        self.main.raise_()
        self.start()

    def setup(self, w, h):
        self.main = QtWidgets.QMainWindow()
        self.main.setFixedSize(w, h)
        self.main.setGeometry(0, 0, w, h)
        self.view = View()
        self.main.setCentralWidget(self.view)
        self.menubar = self.main.menuBar()
        self.statusbar = self.main.statusBar()
        self.toolbar = self.main.addToolBar('Tools')
        self.toolbar.setMovable(False)

    def init(self):
        self.init_menubar()
        self.init_toolbar()
        self.init_sidepanel_left()
        self.init_sidepanel_right()

    def init_menubar(self):
        help_menu = self.menubar.addMenu('&Help')

    def init_toolbar(self):
        self.toolbar.addAction('test', self.controller.test)

    def init_sidepanel_left(self):
        pass

    def init_sidepanel_right(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    viewer = Viewer(800, 600)
