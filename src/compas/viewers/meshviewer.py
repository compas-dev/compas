from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import ctypes

from functools import partial

from numpy import array

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

import compas

from compas.datastructures import Mesh
from compas.geometry import centroid_points
from compas.utilities import hex_to_rgb
from compas.utilities import flatten

from compas.topology import mesh_quads_to_triangles

from compas.viewers.core import xdraw_polygons
from compas.viewers.core import xdraw_lines
from compas.viewers.core import xdraw_points
from compas.viewers.core import xdraw_texts
from compas.viewers.core import xdraw_cylinders
from compas.viewers.core import xdraw_spheres

from compas.viewers.core import Camera
from compas.viewers.core import Mouse
from compas.viewers.core import Grid
from compas.viewers.core import Axes
from compas.viewers.core import GLWidget
from compas.viewers.core import App
from compas.viewers.core import Controller


get_obj_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select OBJ file',
    dir=compas.DATA,
    filter='OBJ files (*.obj)'
)

get_json_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select JSON file',
    dir=compas.DATA,
    filter='JSON files (*.json)'
)

hex_to_rgb = partial(hex_to_rgb, normalize=True)


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MeshViewer', ]


def center_mesh(mesh):
    xyz = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    cx, cy, cz = centroid_points(xyz)
    for key, attr in mesh.vertices(True):
        attr['x'] -= cx
        attr['y'] -= cy


class Front(Controller):

    settings = {}
    settings['vertices.size'] = 0.01
    settings['edges.width'] = 0.01
    settings['vertices.color'] = '#000000'
    settings['edges.color'] = '#666666'
    settings['faces.color:front'] = '#eeeeee'
    settings['faces.color:back'] = '#eeeeee'
    settings['vertices.on'] = True
    settings['edges.on'] = True
    settings['faces.on'] = True
    settings['vertices.labels.on'] = False
    settings['edges.labels.on'] = False
    settings['faces.labels.on'] = False
    settings['vertices.normals.on'] = False
    settings['faces.normals.on'] = False

    def __init__(self, app):
        super(Front, self).__init__(app)
        self.mesh = None

    @property
    def view(self):
        return self.app.view

    def from_obj(self):
        filename, _ = get_obj_file()
        if filename:
            self.mesh = Mesh.from_obj(filename)
            mesh_quads_to_triangles(self.mesh)
            center_mesh(self.mesh)
            self.view.make_buffers()
            self.view.update()

    def from_json(self):
        filename, _ = get_json_file()
        if filename:
            self.mesh = Mesh.from_json(filename)
            mesh_quads_to_triangles(self.mesh)
            center_mesh(self.mesh)
            self.view.make_buffers()
            self.view.update()

    def from_polyhedron(self):
        print('from polyhedron')

    def zoom_extents(self):
        print('zoom extents')

    def zoom_in(self):
        print('zoom in')

    def zoom_out(self):
        print('zoom out')

    def slide_size_vertices(self, value):
        self.settings['vertices.size'] = value
        self.view.update()

    def edit_size_vertices(self, value):
        self.settings['vertices.size'] = value
        self.view.update()

    def toggle_faces(self, state):
        self.settings['faces.on'] = state == QtCore.Qt.Checked
        self.view.update()

    def toggle_edges(self, state):
        self.settings['edges.on'] = state == QtCore.Qt.Checked
        self.view.update()


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
        return self.controller.mesh

    @property
    def settings(self):
        return self.controller.settings

    def paint(self):
        for dl in self.display_lists:
            glCallList(dl)

        self.draw_buffers()

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
            glLineWidth(self.settings['edges.width'])
            glBindBuffer(GL_ARRAY_BUFFER, self.buffers['edges.color'])
            glColorPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffers['edges'])
            glDrawElements(GL_LINES, self.e, GL_UNSIGNED_INT, None)

        if self.settings['vertices.on']:
            pass

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

    def make_buffers(self):
        xyz = list(flatten(self.mesh.get_vertices_attributes('xyz')))
        vertices = list(self.mesh.vertices())
        edges = list(flatten(self.mesh.edges()))
        faces_front = list(flatten(self.mesh.face_vertices(fkey) for fkey in self.mesh.faces()))
        faces_back = list(flatten(self.mesh.face_vertices(fkey)[::-1] for fkey in self.mesh.faces()))
        vertices_color = list(flatten(hex_to_rgb(self.settings['vertices.color']) for key in self.mesh.vertices()))
        edges_color = list(flatten(hex_to_rgb(self.settings['edges.color']) for key in self.mesh.vertices()))
        faces_color_front = list(flatten(hex_to_rgb(self.settings['faces.color:front']) for key in self.mesh.vertices()))
        faces_color_back = list(flatten(hex_to_rgb(self.settings['faces.color:back']) for key in self.mesh.vertices()))

        self.buffers = {
            'xyz'              : self.make_vertex_buffer(xyz, dynamic=False),
            'vertices'         : self.make_element_buffer(vertices, dynamic=False),
            'edges'            : self.make_element_buffer(edges, dynamic=False),
            'faces:front'      : self.make_element_buffer(faces_front, dynamic=False),
            'faces:back'       : self.make_element_buffer(faces_back, dynamic=False),
            'vertices.color'   : self.make_vertex_buffer(vertices_color),
            'edges.color'      : self.make_vertex_buffer(edges_color),
            'faces.color:front': self.make_vertex_buffer(faces_color_front),
            'faces.color:back' : self.make_vertex_buffer(faces_color_back),
        }
        self.n = len(xyz)
        self.v = len(vertices)
        self.e = len(edges)
        self.f = len(faces_front)

    def update_vertex_buffer(self):
        pass

    def update_element_buffer(self):
        pass


class MeshViewer(App):
    """"""

    def __init__(self, config, width=1440, height=900):
        super(MeshViewer, self).__init__()
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
                'text'  : '&Mesh',
                'items' : [
                    {'text' : 'From .obj', 'action': 'from_obj'},
                    {'text' : 'From .json', 'action': 'from_json'}
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
        # 'toolbar': [
        #     {'text': '&Zoom Extents', 'action': 'zoom_extents'},
        #     {'text': '&Zoom In', 'action': 'zoom_in'},
        #     {'text': '&Zoom Out', 'action': 'zoom_out'},
        # ],
        'sidebar': [
            {
                'type'  : 'group',
                'text'  : 'Visibility',
                'items' : [
                    {
                        'type'  : 'group',
                        'text'  : None,
                        'items' : [
                            {'type' : 'checkbox', 'text' : 'vertices', 'action' : None, 'state' : True, },
                            {'type' : 'checkbox', 'text' : 'edges', 'action' : 'toggle_edges', 'state' : True, },
                            {'type' : 'checkbox', 'text' : 'faces', 'action' : 'toggle_faces', 'state' : True, },
                        ]
                    },
                    {
                        'type'  : 'group',
                        'text'  : None,
                        'items' : [
                            {'type' : 'checkbox', 'text' : 'label vertices', 'action' : None, 'state' : True, },
                            {'type' : 'checkbox', 'text' : 'label edges', 'action' : None, 'state' : True, },
                            {'type' : 'checkbox', 'text' : 'label faces', 'action' : None, 'state' : True, },
                        ]
                    }
                ]
            },
            {
                'type' : 'group',
                'text' : 'Appearance',
                'items': [
                    {
                        'type' : 'group',
                        'text' : None,
                        'items': [
                            {'type': 'colorbutton', 'text': 'color vertices', 'value': '#000000', 'action': None, },
                            {'type': 'colorbutton', 'text': 'color edges', 'value': '#000000', 'action': None, },
                            {'type': 'colorbutton', 'text': 'color faces', 'value': '#000000', 'action': None, },
                        ]
                    },
                    {
                        'type' : 'group',
                        'text' : None,
                        'items': [
                            {
                                'type'   : 'slider',
                                'text'   : 'size vertices',
                                'value'  : 0.01,
                                'minval' : 1,
                                'maxval' : 100,
                                'step'   : 1,
                                'scale'  : 0.01,
                                'slide'  : 'slide_size_vertices',
                                'edit'   : 'edit_size_vertices',
                            }
                        ]
                    }
                ]
            }
        ]
    }

    viewer = MeshViewer(config).show()
