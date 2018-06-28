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


# Perhaps zoom should be stored as a zoom factor somewhere.
# Not just as the Z-component of the translation vector.

# Centering should not be handled on the object level,
# but through a base translation vector.


class Camera(object):
    """"""

    def __init__(self, view):
        self.view = view
        self.fov = 60.0
        self.near = 1.0
        self.far = 1000
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
        """Zoom in.

        Notes
        -----
        Zooming in is achieved by moving the objects in the scene closer to the
        camera, i.e. by decreasing the absolute size of the Z-component of the
        translation vector that is applied to all objects.
        """
        self.tz -= steps * self.tz * self.dt

    def zoom_out(self, steps=1):
        """Zoom out.

        Notes
        -----
        Zooming out is achieved by moving the objects in the scene further away
        from the position of the camera, i.e. by increasing the absolute size of
        the Z-component of the translation vector that is used to transform all
        objects.
        """
        self.tz += steps * self.tz * self.dt

    def zoom(self, steps=1):
        """Zoom.

        Notes
        -----
        This is th same as zooming in.

        """
        self.tz -= steps * self.tz * self.dt

    def zoom_extents(self):
        pass

    def rotate(self):
        dx = self.view.mouse.dx()
        dy = self.view.mouse.dy()
        self.rx += self.dr * dy
        self.rz += self.dr * dx

    def translate(self):
        """"""
        dx = self.view.mouse.dx()
        dy = self.view.mouse.dy()
        self.tx += self.dt * dx
        self.ty -= self.dt * dy

    def aim(self):
        """Aim the camera.

        Notes
        -----
        Note that the camera is always positioned in the same location (0, 0, 0)
        and always points in the same direction (-Z). Aiming the camera is
        accomplished by translating and rotating the objects in the scene.

        """
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(self.tx, self.ty, self.tz)

        if self.view.current == self.view.VIEW_PERSPECTIVE:
            glRotatef(self.rx, 1, 0, 0)
            glRotatef(self.rz, 0, 0, 1)

        if self.view.current == self.view.VIEW_FRONT:
            glRotatef(-90, 1, 0, 0)

        if self.view.current == self.view.VIEW_LEFT:
            glRotatef(-90, 1, 0, 0)
            glRotatef(+90, 0, 0, 1)

        if self.view.current == self.view.VIEW_TOP:
            pass

    def focus(self):
        glPushAttrib(GL_TRANSFORM_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.view.current == self.view.VIEW_PERSPECTIVE:
            gluPerspective(self.fov, self.aspect, self.near, self.far)

        else:
            glOrtho(self.tz, -self.tz, self.tz / self.aspect, -self.tz / self.aspect, self.near, self.far)

        glPopAttrib()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
