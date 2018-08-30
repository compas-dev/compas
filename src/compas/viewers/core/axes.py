from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


__all__ = ['Axes']


class Axes(object):
    """"""
    def __init__(self, x_color=None, y_color=None, z_color=None):
        self.x_color = x_color or (1.0, 0.0, 0.0)
        self.y_color = y_color or (0.0, 1.0, 0.0)
        self.z_color = z_color or (0.0, 0.0, 1.0)

    def draw(self):
        x_color = self.x_color
        y_color = self.y_color
        z_color = self.z_color
        glLineWidth(1)
        glBegin(GL_LINES)
        glColor3f(* x_color)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glColor3f(* y_color)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glColor3f(* z_color)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
