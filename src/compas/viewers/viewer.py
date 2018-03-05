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
                'text'  : '&Edit',
                'items' : []
            },
            {
                'type'  : 'menu',
                'text'  : '&View',
                'items' : [
                    {'text' : '&Pan', 'action': None},
                    {'text' : '&Rotate', 'action': None},
                    {
                        'type'  : 'menu',
                        'text'  : '&Zoom',
                        'items' : []
                    },
                    {'type' : 'separator'},
                    {
                        'type'  : 'menu',
                        'text'  : '&Set View',
                        'items' : []
                    },
                    {
                        'type'  : 'menu',
                        'text'  : '&Camera',
                        'items' : []
                    },
                    {
                        'type'  : 'menu',
                        'text'  : '&Grid',
                        'items' : []
                    },
                    {
                        'type'  : 'menu',
                        'text'  : '&Axes',
                        'items' : []
                    },
                    {'type' : 'separator'},
                    {'text' : '&Capture Image', 'action': None},
                    {'text' : '&Capture Video', 'action': None},
                    {'type' : 'separator'}
                ]
            },
            {
                'type'  : 'menu',
                'text'  : '&Tools',
                'items' : []
            },
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
            },
            {
                'type'  : 'menu',
                'text'  : '&Window',
                'items' : []
            },
            {
                'type'  : 'menu',
                'text'  : '&Help',
                'items' : []
            }
        ],
        'toolbar': [
        ],
        'sidebar': [
        ]
    }

    viewer = Viewer(config).show()
