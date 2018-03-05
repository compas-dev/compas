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

    def _clear_lists(self):
        if self.view.faces:
            glDeleteLists(self.view.faces, 1)
        if self.view.edges:
            glDeleteLists(self.view.edges, 1)
        if self.view.vertices:
            glDeleteLists(self.view.vertices, 1)

    def _make_lists(self):
        self._clear_lists()
        key_xyz = {key: self.mesh.vertex_coordinates(key) for key in self.mesh.vertices()}
        self._make_faces_list(key_xyz)
        self._make_edges_list(key_xyz)
        self._make_vertices_list(key_xyz)

    def _make_faces_list(self, key_xyz):
        faces = []
        front = hex_to_rgb(self.settings['faces.color:front'])
        front = list(front) + [1.0]
        back  = hex_to_rgb(self.settings['faces.color:back'])
        back  = list(back) + [1.0]
        for fkey in self.mesh.faces():
            faces.append({'points'      : [key_xyz[key] for key in self.mesh.face_vertices(fkey)],
                          'color.front' : front,
                          'color.back'  : back})
        self.view.faces = glGenLists(1)
        glNewList(self.view.faces, GL_COMPILE)
        xdraw_polygons(faces)
        glEndList()

    def _make_edges_list(self, key_xyz):
        lines = []
        color = hex_to_rgb(self.settings['edges.color'])
        width = self.settings['edges.width']
        for u, v in self.mesh.edges():
            lines.append({'start' : key_xyz[u],
                          'end'   : key_xyz[v],
                          'color' : color,
                          'width' : width})
        self.view.edges = glGenLists(1)
        glNewList(self.view.edges, GL_COMPILE)
        xdraw_cylinders(lines)
        glEndList()

    def _make_vertices_list(self, key_xyz):
        points = []
        color = hex_to_rgb(self.settings['vertices.color'])
        size = self.settings['vertices.size']
        for key in self.mesh.vertices():
            points.append({'pos'   : key_xyz[key],
                           'color' : color,
                           'size'  : size})
        self.view.vertices = glGenLists(1)
        glNewList(self.view.vertices, GL_COMPILE)
        xdraw_spheres(points)
        glEndList()

    def from_obj(self):
        filename, _ = get_obj_file()
        if filename:
            self.mesh = Mesh.from_obj(filename)
            center_mesh(self.mesh)
            self._make_lists()
            self.view.update()

    def from_json(self):
        filename, _ = get_json_file()
        if filename:
            self.mesh = Mesh.from_json(filename)
            center_mesh(self.mesh)
            self._make_lists()
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


class View(GLWidget):
    """"""

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller
        self.faces = None
        self.edges = None
        self.vertices = None

    def __del__(self):
        self.makeCurrent()
        if self.faces:
            glDeleteLists(self.faces, 1)
        if self.edges:
            glDeleteLists(self.edges, 1)
        if self.vertices:
            glDeleteLists(self.vertices, 1)

    @property
    def mesh(self):
        return self.controller.mesh

    @property
    def settings(self):
        return self.controller.settings

    def paint(self):
        if self.settings['faces.on']:
            if self.faces:
                glCallList(self.faces)
        if self.settings['edges.on']:
            if self.edges:
                glCallList(self.edges)
        if self.settings['vertices.on']:
            if self.vertices:
                glCallList(self.vertices)


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
                'text'  : '&Tools',
                'items' : []
            },
            {
                'type'  : 'menu',
                'text'  : '&Mesh',
                'items' : [
                    {'text' : 'From .obj', 'action': 'from_obj'}
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
                            {'type' : 'checkbox', 'text' : 'edges', 'action' : None, 'state' : True, },
                            {'type' : 'checkbox', 'text' : 'faces', 'action' : None, 'state' : True, },
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
