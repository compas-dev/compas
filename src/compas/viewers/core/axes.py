from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Axes', ]


class Axes(object):
    """"""
    def __init__(self, x_colour=None, y_colour=None, z_colour=None):
        self.x_colour = x_colour or (1.0, 0.0, 0.0)
        self.y_colour = y_colour or (0.0, 1.0, 0.0)
        self.z_colour = z_colour or (0.0, 0.0, 1.0)

    def draw(self):
        x_colour = self.x_colour
        y_colour = self.y_colour
        z_colour = self.z_colour
        glLineWidth(1)
        glBegin(GL_LINES)
        glcolour3f(* x_colour)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glcolour3f(* y_colour)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glcolour3f(* z_colour)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
