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
        self.view = View(self.controller)
        self.setup(width, height)
        self.init()



# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    config = {
        'menubar': [
            {
                'type'  : 'menu',
                'text'  : '&Settings',
                'items' : [
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

    viewer = Viewer(config, 800, 600).show()
