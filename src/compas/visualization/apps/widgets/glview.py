from __future__ import print_function

import sys

from PySide.QtCore import Qt
from PySide.QtCore import QPoint

from PySide.QtGui import QApplication
from PySide.QtGui import QColor

from PySide.QtOpenGL import QGLWidget

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from compas.visualization.viewers.drawing import xdraw_polygons
from compas.visualization.viewers.drawing import xdraw_lines
from compas.visualization.viewers.drawing import xdraw_points


# def autoBufferSwap ()
# def bindTexture (fileName)
# def bindTexture (image, target, format, options)
# def bindTexture (image[, target=0x0DE1[, format=0x1908]])
# def bindTexture (pixmap, target, format, options)
# def bindTexture (pixmap[, target=0x0DE1[, format=0x1908]])
# def colormap ()
# def context ()
# def deleteTexture (tx_id)
# def doneCurrent ()
# def doubleBuffer ()
# def drawTexture (point, textureId[, textureTarget=0x0DE1])
# def drawTexture (target, textureId[, textureTarget=0x0DE1])
# def format ()
# def grabFrameBuffer ([withAlpha=false])
# def isSharing ()
# def isValid ()
# def makeCurrent ()
# def makeOverlayCurrent ()
# def overlayContext ()
# def qglClearColor (c)
# def qglColor (c)
# def renderPixmap ([w=0[, h=0[, useContext=false]]])
# def renderText (x, y, str[, fnt=QFont()[, listBase=2000]])
# def renderText (x, y, z, str[, fnt=QFont()[, listBase=2000]])
# def setAutoBufferSwap (on)
# def setColormap (map)
# def swapBuffers ()


# def glDraw ()
# def glInit ()
# def initializeGL ()
# def initializeOverlayGL ()
# def paintGL ()
# def paintOverlayGL ()
# def resizeGL (w, h)
# def resizeOverlayGL (w, h)
# def updateGL ()
# def updateOverlayGL ()


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', 'Shajay Bhooshan']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['GLView', ]


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


class Mouse(object):
    """"""
    def __init__(self, view):
        self.view  = view
        self.pos = QPoint()
        self.last_pos = QPoint()

    def dx(self):
        return self.pos.x() - self.last_pos.x()

    def dy(self):
        return self.pos.y() - self.last_pos.y()


class GLView(QGLWidget):
    """"""

    def __init__(self):
        QGLWidget.__init__(self)
        self.camera = Camera(self)
        self.mouse = Mouse(self)
        self.clear_color = QColor.fromRgb(255, 255, 255)

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

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushAttrib(GL_POLYGON_BIT)
        self.camera.aim()
        self.camera.focus()
        self.paint()
        glPopAttrib()
        glutSwapBuffers()

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
        self.mouse.pos = event.pos()
        if event.buttons() & Qt.LeftButton:
            self.camera.rotate()
            self.mouse.last_pos = event.pos()
            self.updateGL()
        elif event.buttons() & Qt.RightButton:
            self.camera.translate()
            self.mouse.last_pos = event.pos()
            self.updateGL()

    def mousePressEvent(self, event):
        self.mouse.last_pos = event.pos()

    # ==========================================================================
    # keyboard events
    # ==========================================================================

    def keyPressEvent(self, event):
        super(GLView, self).keyPressEvent(event)
        key = event.key()
        self.keyPressAction(key)
        self.updateGL()

    def keyPressAction(self, key):
        raise NotImplementedError

    # ==========================================================================
    # helpers
    # ==========================================================================

    def capture(self, filename, filetype):
        qimage = self.grabFrameBuffer()
        qimage.save(filename, filetype)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures.mesh.mesh import Mesh
    from compas.datastructures.mesh.algorithms import subdivide_mesh_doosabin
    from compas.geometry.elements.polyhedron import Polyhedron


    class View(GLView):

        def __init__(self, mesh, subdfunc):
            super(View, self).__init__()
            self.subdfunc = subdfunc
            self.mesh = mesh
            self.subd = None

        def paint(self):
            key_xyz = {key: self.mesh.vertex_coordinates(key) for key in self.mesh}
            lines = []
            for u, v in self.mesh.edges_iter():
                lines.append({'start' : key_xyz[u],
                              'end'   : key_xyz[v],
                              'color' : (0.1, 0.1, 0.1),
                              'width' : 1.})
            xdraw_lines(lines)
            points = []
            for key in self.mesh:
                points.append({'pos'   : key_xyz[key],
                               'color' : (0.0, 1.0, 0.0),
                               'size'  : 10.0})
            xdraw_points(points)
            if self.subd:
                key_xyz = {key: self.subd.vertex_coordinates(key) for key in self.subd}
                faces   = [self.subd.face_vertices(fkey, True) for fkey in self.subd.face]
                faces   = [[key_xyz[key] for key in vertices] for vertices in faces]
                front   = (0.7, 0.7, 0.7, 1.0)
                back    = (0.2, 0.2, 0.2, 1.0)
                poly    = []
                for points in faces:
                    poly.append({'points'     : points,
                                 'color.front': front,
                                 'color.back' : back})
                lines = []
                for u, v in self.subd.edges_iter():
                    lines.append({'start': key_xyz[u],
                                  'end'  : key_xyz[v],
                                  'color': (0.1, 0.1, 0.1),
                                  'width': 1.})
                xdraw_polygons(poly)
                xdraw_lines(lines)

        def keyPressAction(self, key):
            if key == Qt.Key_1:
                self.subd = self.subdfunc(self.mesh, k=1)
            if key == Qt.Key_2:
                self.subd = self.subdfunc(self.mesh, k=2)
            if key == Qt.Key_3:
                self.subd = self.subdfunc(self.mesh, k=3)
            if key == Qt.Key_4:
                self.subd = self.subdfunc(self.mesh, k=4)
            if key == Qt.Key_5:
                self.subd = self.subdfunc(self.mesh, k=5)



    poly = Polyhedron.generate(6)
    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    app = QApplication(sys.argv)

    view = View(mesh, subdivide_mesh_doosabin)
    view.resize(640, 480)
    view.show()

    sys.exit(app.exec_())
