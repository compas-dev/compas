from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    import PySide2
except ImportError:
    from PySide import QtCore
    from PySide import QtGui
    from PySide import QtOpenGL
    import PySide.QtGui as QtWidgets
    from PySide.QtOpenGL import QGLWidget as QOpenGLWidget
else:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtOpenGL
    from PySide2 import QtWidgets
    # from PySide2.QtWidgets import QOpenGLWidget
    from PySide2.QtOpenGL import QGLWidget as QOpenGLWidget

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

    # make settings a class variable
    # handle all other init stuff on the Controller level

    def __init__(self, app):
        super(Front, self).__init__()
        self.app = app
        self.settings = {}

    @property
    def view(self):
        return self.app.view

    def test(self):
        self.opengl_info()

    def opengl_info(self):
        if self.view:
            print(glGetString(GL_VENDOR))
            print(glGetString(GL_RENDERER))
            print(glGetString(GL_VERSION))
            print(glGetString(GL_SHADING_LANGUAGE_VERSION))
            print(self.view.format().majorVersion())
            print(self.view.context().format().majorVersion())
            extensions = str(glGetString(GL_EXTENSIONS)).split(' ')
            for name in extensions:
                print(name)


class View(GLView):
    """"""

    # same as above

    def __init__(self, controller, gl_format):
        super(View, self).__init__(gl_format)
        self.controller = controller

    @property
    def settings(self):
        return self.controller.settings

    def paint(self):
        pass


class Viewer(App):
    """"""

    def __init__(self, width=1440, height=900):
        super(Viewer, self).__init__()
        self.controller = Front(self)
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

        gl_format = QtOpenGL.QGLFormat()
        gl_format.setVersion(2, 1)
        gl_format.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        gl_format.setSampleBuffers(True)
        gl_format.setDefaultFormat(gl_format)

        self.view = View(self.controller, gl_format)

        self.view.context().setFormat(gl_format)
        self.view.context().create()

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
        opengl_menu = self.menubar.addMenu('&OpenGL')
        opengl_menu.addAction('&Version info', self.controller.opengl_info)
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
