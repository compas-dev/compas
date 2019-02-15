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

from functools import partial

import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.datastructures import mesh_subdivide

from compas.geometry import centroid_points
from compas.utilities import hex_to_rgb
from compas.utilities import flatten
from compas.utilities import pairwise

from compas.viewers.core import Camera
from compas.viewers.core import Mouse
from compas.viewers.core import Grid
from compas.viewers.core import Axes
from compas.viewers.core import GLWidget
from compas.viewers.core import Controller
from compas.viewers.core import App


__author__     = ['Tom Van Mele']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Viewer']


hex_to_rgb = partial(hex_to_rgb, normalize=True)


def flist(items):
    return list(flatten(items))


class MeshView(object):

    def __init__(self, mesh):
        self._mesh = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.mesh = mesh

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return self.mesh.vertices()

    @property
    def faces(self):
        return self._faces

    @property
    def edges(self):
        return self.mesh.edges()

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

        xyz = mesh.get_vertices_attributes('xyz')
        faces = []
        for fkey in mesh.faces():
            fvertices = mesh.face_vertices(fkey)
            f = len(fvertices)
            if f < 3:
                pass
            elif f == 3:
                faces.append(fvertices)
            elif f == 4:
                a, b, c, d = fvertices
                faces.append([a, b, c])
                faces.append([c, d, a])
            else:
                o = mesh.face_centroid(fkey)
                v = len(xyz)
                xyz.append(o)
                for a, b in pairwise(fvertices + fvertices[0:1]):
                    faces.append([a, b, v])

        self._xyz = xyz
        self._faces = faces


class Front(Controller):
    """"""

    settings = {}
    settings['vertices.size:value'] = 1.0
    settings['vertices.size:minval'] = 1
    settings['vertices.size:maxval'] = 100
    settings['vertices.size:step'] = 1
    settings['vertices.size:scale'] = 0.1

    settings['edges.width:value'] = 1.0
    settings['edges.width:minval'] = 1
    settings['edges.width:maxval'] = 100
    settings['edges.width:step'] = 1
    settings['edges.width:scale'] = 0.1

    settings['normals.scale:value'] = 1.0
    settings['normals.scale:minval'] = 1
    settings['normals.scale:maxval'] = 100
    settings['normals.scale:step'] = 1
    settings['normals.scale:scale'] = 0.1

    settings['vertices.color'] = '#0092d2'
    settings['edges.color'] = '#666666'
    settings['faces.color:front'] = '#eeeeee'
    settings['faces.color:back'] = '#ff5e99'
    settings['normals.color'] = '#0092d2'

    settings['vertices.on'] = True
    settings['edges.on'] = True
    settings['faces.on'] = True

    settings['normals.on'] = False

    settings['vertices.labels.on'] = False
    settings['edges.labels.on'] = False
    settings['faces.labels.on'] = False

    settings['camera.elevation:value'] = -60
    settings['camera.elevation:minval'] = -180
    settings['camera.elevation:maxval'] = 0
    settings['camera.elevation:step'] = +1
    settings['camera.elevation:scale'] = +1

    settings['camera.azimuth:value'] = +30
    settings['camera.azimuth:minval'] = -180
    settings['camera.azimuth:maxval'] = +180
    settings['camera.azimuth:step'] = +1
    settings['camera.azimuth:scale'] = +1

    settings['camera.distance:value'] = +10
    settings['camera.distance:minval'] = 0
    settings['camera.distance:maxval'] = +100
    settings['camera.distance:step'] = +1
    settings['camera.distance:scale'] = +1
    settings['camera.distance:delta'] = +0.05

    settings['camera.rotation:delta'] = +0.5
    settings['camera.fov:value'] = 50
    settings['camera.near:value'] = 0.1
    settings['camera.far:value'] = 1000

    def __init__(self, app):
        super(Front, self).__init__(app)
        self._mesh = None
        self._meshview = None

    @property
    def view(self):
        return self.app.view

    @property
    def mesh(self):
        return self._mesh

    @property
    def meshview(self):
        return self._meshview

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh
        self._meshview = MeshView(mesh)

    # centering the mesh should be handled
    # by storing a base translation vector for the camera
    def center_mesh(self):
        xyz = [self.mesh.vertex_coordinates(key) for key in self.mesh.vertices()]
        cx, cy, cz = centroid_points(xyz)
        for key, attr in self.mesh.vertices(True):
            attr['x'] -= cx
            attr['y'] -= cy


class View(GLWidget):
    """"""

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller
        self.n = 0
        self.v = 0
        self.e = 0
        self.f = 0

    @property
    def mesh(self):
        return self.controller.meshview

    @property
    def settings(self):
        return self.controller.settings

    # ==========================================================================
    # arrays
    # ==========================================================================

    # move this to model?

    @property
    def array_xyz(self):
        return flist(self.mesh.xyz)

    @property
    def array_vertices(self):
        return list(self.mesh.vertices)

    @property
    def array_edges(self):
        return flist(self.mesh.edges)

    @property
    def array_faces_front(self):
        return flist(self.mesh.faces)

    @property
    def array_faces_back(self):
        return flist(face[::-1] for face in self.mesh.faces)

    @property
    def array_vertices_color(self):
        return flist(hex_to_rgb(self.settings['vertices.color']) for key in self.mesh.vertices)

    @property
    def array_edges_color(self):
        return flist(hex_to_rgb(self.settings['edges.color']) for key in self.mesh.vertices)

    @property
    def array_faces_color_front(self):
        return flist(hex_to_rgb(self.settings['faces.color:front']) for key in self.mesh.xyz)

    @property
    def array_faces_color_back(self):
        return flist(hex_to_rgb(self.settings['faces.color:back']) for key in self.mesh.xyz)

    # ==========================================================================
    # painting
    # ==========================================================================

    def paint(self):
        for dl in self.display_lists:
            glCallList(dl)

        self.draw_buffers()

    def make_buffers(self):
        self.buffers = {
            'xyz'              : self.make_vertex_buffer(self.array_xyz),
            'vertices'         : self.make_index_buffer(self.array_vertices),
            'edges'            : self.make_index_buffer(self.array_edges),
            'faces:front'      : self.make_index_buffer(self.array_faces_front),
            'faces:back'       : self.make_index_buffer(self.array_faces_back),
            'vertices.color'   : self.make_vertex_buffer(self.array_vertices_color, dynamic=True),
            'edges.color'      : self.make_vertex_buffer(self.array_edges_color, dynamic=True),
            'faces.color:front': self.make_vertex_buffer(self.array_faces_color_front, dynamic=True),
            'faces.color:back' : self.make_vertex_buffer(self.array_faces_color_back, dynamic=True),
        }
        self.n = len(self.array_xyz)
        self.v = len(self.array_vertices)
        self.e = len(self.array_edges)
        self.f = len(self.array_faces_front)

    def draw_buffers(self):
        if not self.buffers:
            return

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers['xyz'])
        glVertexPointer(3, GL_FLOAT, 0, None)

        if self.settings['faces.on']:
            glBindBuffer(GL_ARRAY_BUFFER, self.buffers['faces.color:front'])
            glColorPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffers['faces:front'])
            glDrawElements(GL_TRIANGLES, self.f, GL_UNSIGNED_INT, None)

            glBindBuffer(GL_ARRAY_BUFFER, self.buffers['faces.color:back'])
            glColorPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffers['faces:back'])
            glDrawElements(GL_TRIANGLES, self.f, GL_UNSIGNED_INT, None)

        if self.settings['edges.on']:
            glLineWidth(self.settings['edges.width:value'])
            glBindBuffer(GL_ARRAY_BUFFER, self.buffers['edges.color'])
            glColorPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffers['edges'])
            glDrawElements(GL_LINES, self.e, GL_UNSIGNED_INT, None)

        if self.settings['vertices.on']:
            glPointSize(self.settings['vertices.size:value'])
            glBindBuffer(GL_ARRAY_BUFFER, self.buffers['vertices.color'])
            glColorPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffers['vertices'])
            glDrawElements(GL_POINTS, self.v, GL_UNSIGNED_INT, None)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)


class Viewer(App):
    """"""

    def __init__(self, config=None, style=None):
        config = config or {}
        super(Viewer, self).__init__(config, style)
        self.config = config
        self.controller = Front(self)
        self.view = View(self.controller)
        self.setup()
        self.init()

    @property
    def mesh(self):
        return self.controller.mesh

    @mesh.setter
    def mesh(self, mesh):
        self.controller.mesh = mesh
        self.controller.center_mesh()

        self.view.glInit()
        self.view.make_buffers()
        self.view.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    viewer = Viewer()

    viewer.mesh = Mesh.from_polyhedron(6)

    viewer.show()
