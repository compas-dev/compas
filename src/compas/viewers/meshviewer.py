from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

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


class MeshViewer(App):
    """"""

    def __init__(self, config, width=1440, height=900):
        super(MeshViewer, self).__init__()
        self.config = config
        self.controller = Front(self)
        self.view = View(self.controller)
        self.setup(width, height)
        self.init()


class Front(Controller):

    settings = {}
    settings['vertices.size:value'] = 1.0
    settings['vertices.size:minval'] = 1
    settings['vertices.size:maxval'] = 100
    settings['vertices.size:step'] = 1
    settings['vertices.size:scale'] = 0.1
    settings['edges.width:value'] = 1.0
    settings['edges.width:minval'] = 1
    settings['edges.width:maxval'] = 10
    settings['edges.width:step'] = 1
    settings['edges.width:scale'] = 1.0
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

    def center_mesh(self):
        xyz = [self.mesh.vertex_coordinates(key) for key in self.mesh.vertices()]
        cx, cy, cz = centroid_points(xyz)
        for key, attr in self.mesh.vertices(True):
            attr['x'] -= cx
            attr['y'] -= cy

    def from_obj(self):
        filename, _ = get_obj_file()
        if filename:
            self.mesh = Mesh.from_obj(filename)
            mesh_quads_to_triangles(self.mesh)
            self.center_mesh()
            self.view.make_buffers()
            self.view.update()

    def from_json(self):
        filename, _ = get_json_file()
        if filename:
            self.mesh = Mesh.from_json(filename)
            mesh_quads_to_triangles(self.mesh)
            self.center_mesh()
            self.view.make_buffers()
            self.view.update()

    def from_polyhedron(self, f):
        self.mesh = Mesh.from_polyhedron(f)
        mesh_quads_to_triangles(self.mesh)
        self.center_mesh()
        self.view.make_buffers()
        self.view.update()

    def zoom_extents(self):
        print('zoom extents')

    def zoom_in(self):
        print('zoom in')

    def zoom_out(self):
        print('zoom out')

    def slide_size_vertices(self, value):
        self.settings['vertices.size:value'] = value
        self.view.update()

    def edit_size_vertices(self, value):
        self.settings['vertices.size:value'] = value
        self.view.update()

    def slide_width_edges(self, value):
        self.settings['edges.width:value'] = value
        self.view.update()

    def edit_width_edges(self, value):
        self.settings['edges.width:value'] = value
        self.view.update()

    def toggle_faces(self, state):
        self.settings['faces.on'] = state == QtCore.Qt.Checked
        self.view.update()

    def toggle_edges(self, state):
        self.settings['edges.on'] = state == QtCore.Qt.Checked
        self.view.update()

    def toggle_vertices(self, state):
        self.settings['vertices.on'] = state == QtCore.Qt.Checked
        self.view.update()

    def change_vertices_color(self, color):
        self.settings['vertices.color'] = color
        self.view.update_vertex_buffer('vertices.color', self.view.vertices_color)
        self.view.update()
        self.app.main.activateWindow()

    def change_edges_color(self, color):
        self.settings['edges.color'] = color
        self.view.update_vertex_buffer('edges.color', self.view.edges_color)
        self.view.update()
        self.app.main.activateWindow()

    def change_faces_color_front(self, color):
        self.settings['faces.color:front'] = color
        self.view.update_vertex_buffer('faces.color:front', self.view.faces_color_front)
        self.view.update()
        self.app.main.activateWindow()

    def change_faces_color_back(self, color):
        self.settings['faces.color:back'] = color
        self.view.update_vertex_buffer('faces.color:back', self.view.faces_color_back)
        self.view.update()
        self.app.main.activateWindow()


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
    def xyz(self):
        return list(flatten(self.mesh.get_vertices_attributes('xyz')))

    @property
    def vertices(self):
        return list(self.mesh.vertices())

    @property
    def edges(self):
        return list(flatten(self.mesh.edges()))

    @property
    def faces_front(self):
        return list(flatten(self.mesh.face_vertices(fkey) for fkey in self.mesh.faces()))

    @property
    def faces_back(self):
        return list(flatten(self.mesh.face_vertices(fkey)[::-1] for fkey in self.mesh.faces()))

    @property
    def vertices_color(self):
        return list(flatten(hex_to_rgb(self.settings['vertices.color']) for key in self.mesh.vertices()))

    @property
    def edges_color(self):
        return list(flatten(hex_to_rgb(self.settings['edges.color']) for key in self.mesh.vertices()))

    @property
    def faces_color_front(self):
        return list(flatten(hex_to_rgb(self.settings['faces.color:front']) for key in self.mesh.vertices()))

    @property
    def faces_color_back(self):
        return list(flatten(hex_to_rgb(self.settings['faces.color:back']) for key in self.mesh.vertices()))

    @property
    def settings(self):
        return self.controller.settings

    def paint(self):
        for dl in self.display_lists:
            glCallList(dl)

        self.draw_buffers()

    def make_buffers(self):
        self.buffers = {
            'xyz'              : self.make_vertex_buffer(self.xyz, dynamic=False),
            'vertices'         : self.make_element_buffer(self.vertices, dynamic=False),
            'edges'            : self.make_element_buffer(self.edges, dynamic=False),
            'faces:front'      : self.make_element_buffer(self.faces_front, dynamic=False),
            'faces:back'       : self.make_element_buffer(self.faces_back, dynamic=False),
            'vertices.color'   : self.make_vertex_buffer(self.vertices_color),
            'edges.color'      : self.make_vertex_buffer(self.edges_color),
            'faces.color:front': self.make_vertex_buffer(self.faces_color_front),
            'faces.color:back' : self.make_vertex_buffer(self.faces_color_back),
        }
        self.n = len(self.xyz)
        self.v = len(self.vertices)
        self.e = len(self.edges)
        self.f = len(self.faces_front)

    def update_vertex_buffer(self, name, data):
        self.buffers[name] = self.make_vertex_buffer(data, dynamic=True)

    def update_element_buffer(self):
        pass

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    config = {
        'menubar': [
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
                    {'text' : 'From .json', 'action': 'from_json'},
                    {'type' : 'separator'},
                    {
                        'type' : 'menu',
                        'text' : 'From Polyhedron',
                        'items': [
                            {'text': 'Tetrahedron', 'action': 'from_polyhedron', 'args': [4]},
                            {'text': 'Hexahedron', 'action': 'from_polyhedron', 'args': [6]},
                            {'text': 'Octahedron', 'action': 'from_polyhedron', 'args': [8]},
                            {'text': 'Dodecahedron', 'action': 'from_polyhedron', 'args': [12]},
                        ]
                    },
                    {'type' : 'separator'},
                ]
            },
            {
                'type'  : 'menu',
                'text'  : '&Tools',
                'items' : [
                ]
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
                            {'type' : 'checkbox', 'text' : 'vertices', 'action' : 'toggle_vertices', 'state' : True, },
                            {'type' : 'checkbox', 'text' : 'edges', 'action' : 'toggle_edges', 'state' : True, },
                            {'type' : 'checkbox', 'text' : 'faces', 'action' : 'toggle_faces', 'state' : True, },
                        ]
                    },
                    # {
                    #     'type'  : 'group',
                    #     'text'  : None,
                    #     'items' : [
                    #         {'type' : 'checkbox', 'text' : 'label vertices', 'action' : None, 'state' : True, },
                    #         {'type' : 'checkbox', 'text' : 'label edges', 'action' : None, 'state' : True, },
                    #         {'type' : 'checkbox', 'text' : 'label faces', 'action' : None, 'state' : True, },
                    #     ]
                    # }
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
                            {
                                'type'  : 'colorbutton',
                                'text'  : 'color vertices',
                                'value' : Front.settings['vertices.color'],
                                'action': 'change_vertices_color',
                            },
                            {
                                'type'  : 'colorbutton',
                                'text'  : 'color edges',
                                'value' : Front.settings['edges.color'],
                                'action': 'change_edges_color',
                            },
                            {
                                'type'  : 'colorbutton',
                                'text'  : 'color faces (front)',
                                'value' : Front.settings['faces.color:front'],
                                'action': 'change_faces_color_front',
                            },
                            {
                                'type'  : 'colorbutton',
                                'text'  : 'color faces (back)',
                                'value' : Front.settings['faces.color:back'],
                                'action': 'change_faces_color_back',
                            },
                        ]
                    },
                    {
                        'type' : 'group',
                        'text' : None,
                        'items': [
                            {
                                'type'   : 'slider',
                                'text'   : 'size vertices',
                                'value'  : Front.settings['vertices.size:value'],
                                'minval' : Front.settings['vertices.size:minval'],
                                'maxval' : Front.settings['vertices.size:maxval'],
                                'step'   : Front.settings['vertices.size:step'],
                                'scale'  : Front.settings['vertices.size:scale'],
                                'slide'  : 'slide_size_vertices',
                                'edit'   : 'edit_size_vertices',
                            },
                            {
                                'type'   : 'slider',
                                'text'   : 'width edges',
                                'value'  : Front.settings['edges.width:value'],
                                'minval' : Front.settings['edges.width:minval'],
                                'maxval' : Front.settings['edges.width:maxval'],
                                'step'   : Front.settings['edges.width:step'],
                                'scale'  : Front.settings['edges.width:scale'],
                                'slide'  : 'slide_width_edges',
                                'edit'   : 'edit_width_edges',
                            }
                        ]
                    }
                ]
            }
        ]
    }

    viewer = MeshViewer(config).show()
