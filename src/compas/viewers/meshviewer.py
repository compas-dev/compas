from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    import PySide2
except ImportError:
    from PySide import QtCore
    from PySide import QtGui
else:
    from PySide2 import QtCore
    from PySide2 import QtGui

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from compas.viewers.core import Camera
from compas.viewers.core import Mouse
from compas.viewers.core import Grid
from compas.viewers.core import Axes
from compas.viewers.core import GLView

from compas.viewers.core.app import App
from compas.viewers.core.controller import Controller


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MeshViewer', ]


class Front(Controller):
    """"""

    def __init__(self):
        pass

    def from_obj(self):
        print('from obj')

    def zoom_extents(self):
        print('zoom extents')

    def zoom_in(self):
        print('zoom in')

    def zoom_out(self):
        print('zoom out')


class View(GLView):
    """"""

    def __init__(self):
        super(View, self).__init__()

    def paint(self):
        pass


class MeshViewer(App):
    """"""

    def __init__(self, width=1440, height=900):
        super(MeshViewer, self).__init__()
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
        self.main = QtGui.QMainWindow()
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
        model_menu = self.menubar.addMenu('&Model')
        view_menu = self.menubar.addMenu('&View')
        help_menu = self.menubar.addMenu('&Help')
        model_menu.addAction('&From OBJ', self.controller.from_obj)

    def init_toolbar(self):
        self.toolbar.addAction('zoom extents', self.controller.zoom_extents)
        self.toolbar.addAction('zoom in', self.controller.zoom_in)
        self.toolbar.addAction('zoom out', self.controller.zoom_out)

    def init_sidepanel_left(self):
        pass

    def init_sidepanel_right(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    viewer = MeshViewer()
