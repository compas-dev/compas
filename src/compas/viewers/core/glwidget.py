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


__all__ = ['GLWidget']


# http://docs.gl/gl4/glDebugMessageCallback


class GLWidget(QOpenGLWidget):
    """"""

    VIEW_PERSPECTIVE = 1
    VIEW_FRONT = 2
    VIEW_LEFT = 3
    VIEW_TOP = 4

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent=parent)

        self._current_view = GLWidget.VIEW_PERSPECTIVE

        self.camera = Camera(self)
        self.mouse = Mouse(self)
        self.clear_color = QtGui.QColor.fromRgb(255, 255, 255)
        self.display_lists = []
        self.buffers = []

    @property
    def current(self):
        return self._current_view

    @current.setter
    def current(self, value):
        self._current_view = value

    def get_error(self):
        return glGetError()

    # ==========================================================================
    # buffers
    # ==========================================================================

    def make_vertex_buffer(self, data, dynamic=False):
        d = len(data)
        b = glGenBuffers(1)
        cdata = (ctypes.c_float * d)(* data)
        usage = GL_DYNAMIC_DRAW if dynamic else GL_STATIC_DRAW
        glBindBuffer(GL_ARRAY_BUFFER, b)
        glBufferData(GL_ARRAY_BUFFER, 4 * d, cdata, usage)
        return b

    def make_index_buffer(self, indices, dynamic=False):
        i = len(indices)
        b = glGenBuffers(1)
        cindices = (ctypes.c_uint * i)(* indices)
        usage = GL_DYNAMIC_DRAW if dynamic else GL_STATIC_DRAW
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * i, cindices, usage)
        return b

    def update_vertex_buffer(self, name, data):
        self.buffers[name] = self.make_vertex_buffer(data, dynamic=True)

    def update_index_buffer(self, name, indices):
        self.buffers[name] = self.make_index_buffer(indices, dynamic=True)

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
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
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

    def paint(self):
        raise NotImplementedError

    # ==========================================================================
    # resize callback
    # ==========================================================================

    def resizeEvent(self, event):
        # super(GLWidget, self).resizeEvent(event)
        w = event.size().width()
        h = event.size().height()
        glViewport(0, 0, w, h)

    def resizeGl(self, w, h):
        glViewport(0, 0, w, h)
        self.camera.aim()
        self.camera.focus()

    # ==========================================================================
    # mouse events
    # ==========================================================================

    def mouseMoveEvent(self, event):
        if self.isActiveWindow() and self.underMouse():
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
        if self.isActiveWindow() and self.underMouse():
            self.mouse.last_pos = event.pos()

    def wheelEvent(self, event):
        if self.isActiveWindow() and self.underMouse():
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

    import sys

    app = QtGui.QApplication(sys.argv)
    
    w = GLWidget()
    w.show()

    app.exec_()
