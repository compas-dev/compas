from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['Camera', ]


class Camera(object):
    """"""
    def __init__(self, view):
        self.view = view
        self.fov = 60.0
        self.near = 1.0
        self.far = 100
        self.rx = -60.0  # from y to z => pos
        self.rz = +45.0  # from x to y => pos
        self.dr = +0.5
        self.tx = +0.0
        self.ty = +0.0
        self.tz = -10.0  # move the scene away from the camera
        self.dt = +0.05

    @property
    def aspect(self):
        w = self.view.width()
        h = self.view.height()
        return float(w) / float(h)

    def zoom_in(self, steps=1):
        self.tz -= steps * self.tz * self.dt

    def zoom_out(self, steps=1):
        self.tz += steps * self.tz * self.dt

    def zoom(self, steps=1):
        self.tz -= steps * self.tz * self.dt

    def rotate(self):
        dx = self.view.mouse.dx()
        dy = self.view.mouse.dy()
        self.rx += self.dr * dy
        self.rz += self.dr * dx

    def translate(self):
        dx = self.view.mouse.dx()
        dy = self.view.mouse.dy()
        self.tx += self.dt * dx
        self.ty -= self.dt * dy

    def aim(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.tx, self.ty, self.tz)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.rz, 0, 0, 1)

    def focus(self):
        glPushAttrib(GL_TRANSFORM_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.aspect, self.near, self.far)
        glPopAttrib()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
