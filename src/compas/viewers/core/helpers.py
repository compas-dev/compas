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


__all__ = [
    'Axes',
    'Camera',
    'Grid',
    'Mouse'
]


class Arrow(object):
    pass


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
        glLineWidth(3)
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


class Camera(object):
    """"""
    def __init__(self, viewer):
        self.viewer = viewer
        self.rx = -60.0  # from y to z => pos
        self.rz = +30.0  # from x to y => pos
        self.dr = +0.5
        self.tx = +0.0
        self.ty = +0.0
        self.tz = -20.0  # move the scene away from the camera
        self.dt = +0.1

    def update(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.tx, self.ty, self.tz)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.rz, 0, 0, 1)

    def zoom_in(self, steps=1):
        for i in range(steps):
            self.tz -= self.tz * self.dt

    def zoom_out(self, steps=1):
        for i in range(steps):
            self.tz += self.tz * self.dt


class Grid(object):
    """"""
    def __init__(self):
        self.xlim = -10, 10
        self.ylim = -10, 10
        self.linewidth = 1
        self.color = (0, 0, 0)
        self.dotted = True

    def draw(self):
        glColor3f(*self.color)
        glLineWidth(self.linewidth)
        if self.dotted:
            glEnable(GL_LINE_STIPPLE)
            glLineStipple(1, 0xAAAA)
        glBegin(GL_LINES)
        for i in range(self.xlim[0], self.xlim[1] + 1):
            glVertex3f(i, self.ylim[0], 0)
            glVertex3f(i, self.ylim[1], 0)
        for i in range(self.ylim[0], self.ylim[1] + 1):
            glVertex3f(self.xlim[0], i, 0)
            glVertex3f(self.xlim[1], i, 0)
        glEnd()
        if self.dotted:
            glDisable(GL_LINE_STIPPLE)


class Mouse(object):
    """"""
    def __init__(self, viewer):
        self.viewer  = viewer
        self.buttons = [False, False, False, False, False]
        self.x       = 0.0
        self.y       = 0.0
        self.x_last  = 0.0
        self.y_last  = 0.0


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
