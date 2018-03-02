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
from OpenGL.GLUT import *
from OpenGL.GLU import *

from compas.viewers.core import Camera
from compas.viewers.core import Mouse


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['GLWidget', ]


class GLWidget(QOpenGLWidget):
    """"""

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent=parent)
        # add these to the controller?
        self.camera = Camera(self)
        self.mouse = Mouse(self)
        self.clear_color = QtGui.QColor.fromRgb(255, 255, 255)

    # ==========================================================================
    # inititlisation
    # ==========================================================================

    def initializeGL(self):
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        self.qglClearColor(self.clear_color)
        glCullFace(GL_BACK)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPolygonOffset(1.0, 1.0)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_CULL_FACE)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        self.camera.aim()
        self.camera.focus()

    # ==========================================================================
    # paint callback
    # ==========================================================================

    # https://stackoverflow.com/questions/35854076/pyqt5-opengl-4-1-core-profile-invalid-frame-buffer-operation-mac-os
    # https://stackoverflow.com/questions/11089561/opengl-invalid-framebuffer-operation-after-glcleargl-color-buffer-bit
    # https://www.khronos.org/registry/OpenGL-Refpages/es2.0/xhtml/glCheckFramebufferStatus.xml

    def paintGL(self):
        if not self.isValid():
            return
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushAttrib(GL_POLYGON_BIT)
        self.camera.aim()
        self.camera.focus()
        self.paint()
        glPopAttrib()
        # glutSwapBuffers()

    def paint(self):
        raise NotImplementedError

    # ==========================================================================
    # resize callback
    # ==========================================================================

    def resizeGl(self, w, h):
        glViewport(0, 0, w, h)
        self.camera.aim()
        self.camera.focus()

    # ==========================================================================
    # mouse events
    # ==========================================================================

    def mouseMoveEvent(self, event):
        if self.underMouse():
            self.mouse.pos = event.pos()
            if event.buttons() & QtCore.Qt.LeftButton:
                self.camera.rotate()
                self.mouse.last_pos = event.pos()
                self.update()
            elif event.buttons() & QtCore.Qt.RightButton:
                self.camera.translate()
                self.mouse.last_pos = event.pos()
                self.update()

    def mousePressEvent(self, event):
        if self.underMouse():
            self.mouse.last_pos = event.pos()

    def wheelEvent(self, event):
        if self.underMouse():
            degrees = event.delta() / 8
            steps = degrees / 15
            self.camera.zoom(steps)
            self.update()

    # ==========================================================================
    # keyboard events
    # ==========================================================================

    def keyPressEvent(self, event):
        super(GLWidget, self).keyPressEvent(event)
        key = event.key()
        self.keyPressAction(key)
        self.update()

    def keyPressAction(self, key):
        raise NotImplementedError

    # ==========================================================================
    # helpers
    # ==========================================================================

    def capture(self, filename, filetype):
        qimage = self.grabFrameBuffer()
        qimage.save(filename, filetype)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
