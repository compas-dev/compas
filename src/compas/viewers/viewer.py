from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

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

    # make settings a class variable
    # handle all other init stuff on the Controller level

    def __init__(self, app):
        super(Front, self).__init__()
        self.app = app
        self.settings = {}

    @property
    def view(self):
        return self.app.view

    def opengl_version_info(self):
        print(glGetString(GL_VENDOR))
        print(glGetString(GL_RENDERER))
        print(glGetString(GL_VERSION))
        print(glGetString(GL_SHADING_LANGUAGE_VERSION))
        print(self.view.format().majorVersion())
        print(self.view.context().format().majorVersion())

    def opengl_extensions(self):
        extensions = str(glGetString(GL_EXTENSIONS)).split(' ')
        for name in extensions:
            print(name)

    def opengl_set_version(self, version):
        major, minor = version
        gl_format = QtOpenGL.QGLFormat()
        gl_format.setVersion(major, minor)
        gl_format.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        gl_format.setSampleBuffers(True)
        gl_format.setDefaultFormat(gl_format)
        self.view.context().setFormat(gl_format)
        self.view.context().create()
        self.view.glInit()


class View(GLWidget):
    """"""

    # same as above

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

    def __init__(self, config, width=1440, height=900):
        super(Viewer, self).__init__()
        self.config = config
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

        self.view = View(self.controller)

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
        def make_menu(menu, parent):
            for item in menu:
                mtype = item.get('type', None)
                if mtype == 'separator':
                    parent.addSeparator()
                    continue
                if mtype == 'menu':
                    newmenu = parent.addMenu(item['text'])
                    items = item.get('items')
                    if items:
                        make_menu(items, newmenu)
                    continue
                action = parent.addAction(item['text'])
                handler = item.get('action', None)
                if handler:
                    if hasattr(self.controller, handler):
                        handler = getattr(self.controller, handler)
                        args = item.get('args', [])
                        kwargs = item.get('kwargs', {})
                        if args or kwargs:
                            handler = partial(handler, *args, **kwargs)
                        action.triggered.connect(handler)
        if not self.config:
            return
        if 'menubar' not in self.config:
            return
        make_menu(self.config['menubar'], self.menubar)

    def init_toolbar(self):
        pass

    def init_sidepanel_left(self):
        pass

    def init_sidepanel_right(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    config = {
        'menubar': [
            {
                'type'  : 'menu',
                'text'  : '&Viewer',
                'items' : [
                    {'text' : '&Info', 'action' : None},
                    {
                        'type'  : 'menu',
                        'text'  : '&OpenGL',
                        'items' : [
                            {'text' : '&Version Info', 'action': 'opengl_version_info'},
                            {'text' : '&Extensions', 'action': 'opengl_extensions'},
                            {'type' : 'separator'},
                            {'text' : '&Set Version 2.1', 'action': 'opengl_set_version', 'args': [(2, 1), ]},
                            {'text' : '&Set Version 3.3', 'action': 'opengl_set_version', 'args': [(3, 3), ]},
                            {'text' : '&Set Version 4.1', 'action': 'opengl_set_version', 'args': [(4, 1), ]}
                        ]
                    }
                ]
            },
            {
                'type'  : 'menu',
                'text'  : '&File',
                'items' : [
                    {'text' : '&New', 'action' : None},
                    {'text' : '&Open', 'action' : None},
                    {'type' : 'separator'},
                    {'text' : '&Save', 'action' : None},
                    {'text' : '&Save As', 'action' : None}
                ]
            },
            {
                'type'  : 'menu',
                'text'  : '&View',
                'items' : []
            },
            {
                'type'  : 'menu',
                'text'  : '&Help',
                'items' : []
            }
        ]
    }

    viewer = Viewer(config, 800, 600)
