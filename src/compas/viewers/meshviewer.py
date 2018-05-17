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

# from compas.topology import mesh_quads_to_triangles
from compas.topology import mesh_flip_cycles
from compas.topology import mesh_subdivide

# from compas.viewers.core import Camera
# from compas.viewers.core import Mouse
# from compas.viewers.core import Grid
# from compas.viewers.core import Axes

from compas.viewers.core import GLWidget
from compas.viewers.core import App
from compas.viewers.core import Controller


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MeshViewer', ]


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


def flist(items):
    return list(flatten(items))


class MeshViewer(App):
    """"""

    def __init__(self, config, style):
        super(MeshViewer, self).__init__(config, style)
        # setting the MVC components should be done explicitly
        self.controller = Front(self)
        self.view = View(self.controller)
        self.setup()
        self.init()


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

    # ==========================================================================
    # arrays
    # ==========================================================================

    @property
    def faces(self):
        faces = []
        for fkey in self.mesh.faces():
            vertices = self.mesh.face_vertices(fkey)
            if len(vertices) == 3:
                faces.append(vertices)
                continue
            if len(vertices) == 4:
                a, b, c, d = vertices
                faces.append([a, b, c])
                faces.append([c, d, a])
                continue
            raise NotImplementedError
        return faces

    @property
    def array_xyz(self):
        return flist(self.mesh.get_vertices_attributes('xyz'))

    @property
    def array_vertices(self):
        return list(self.mesh.vertices())

    @property
    def array_edges(self):
        return flist(self.mesh.edges())

    @property
    def array_faces_front(self):
        return flist(self.faces)

    @property
    def array_faces_back(self):
        return flist(face[::-1] for face in self.faces)

    @property
    def array_vertices_color(self):
        return flist(hex_to_rgb(self.settings['vertices.color']) for key in self.mesh.vertices())

    @property
    def array_edges_color(self):
        return flist(hex_to_rgb(self.settings['edges.color']) for key in self.mesh.vertices())

    @property
    def array_faces_color_front(self):
        return flist(hex_to_rgb(self.settings['faces.color:front']) for key in self.mesh.vertices())

    @property
    def array_faces_color_back(self):
        return flist(hex_to_rgb(self.settings['faces.color:back']) for key in self.mesh.vertices())

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


class Front(Controller):

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

    def __init__(self, app):
        super(Front, self).__init__(app)
        self.mesh = None

    @property
    def view(self):
        return self.app.view

    # centering the mesh should be handled
    # by storing a base translation vector for the camera
    def center_mesh(self):
        xyz = [self.mesh.vertex_coordinates(key) for key in self.mesh.vertices()]
        cx, cy, cz = centroid_points(xyz)
        for key, attr in self.mesh.vertices(True):
            attr['x'] -= cx
            attr['y'] -= cy

    # ==========================================================================
    # constructors
    # ==========================================================================

    def from_obj(self):
        filename, _ = get_obj_file()
        if filename:
            self.mesh = Mesh.from_obj(filename)
            self.center_mesh()
            self.view.make_buffers()
            self.view.update()

    def from_json(self):
        filename, _ = get_json_file()
        if filename:
            self.mesh = Mesh.from_json(filename)
            self.center_mesh()
            self.view.make_buffers()
            self.view.update()

    def to_obj(self):
        self.message('Export to OBJ is under construction...')

    def to_json(self):
        self.message('Export to JSON is under construction...')

    def from_polyhedron(self, f):
        self.mesh = Mesh.from_polyhedron(f)
        self.center_mesh()
        self.view.make_buffers()
        self.view.update()

    # ==========================================================================
    # view
    # ==========================================================================

    def zoom_extents(self):
        self.message('Zoom Extents is under construction...')

    def zoom_in(self):
        self.view.camera.zoom_in()
        self.view.update()

    def zoom_out(self):
        self.view.camera.zoom_out()
        self.view.update()

    def set_view(self, view):
        self.view.current = view
        self.view.update()

    def update_camera_settings(self):
        self.log('Updating the camera settings.')

    def capture_image(self):
        self.message('Capture Image is under construction...')

    def capture_video(self):
        self.message('Capture Video is under construction...')

    # ==========================================================================
    # appearance
    # ==========================================================================

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

    def slide_scale_normals(self, value):
        self.settings['normals.scale:value'] = value
        self.view.update()

    def edit_scale_normals(self, value):
        self.settings['normals.scale:value'] = value
        self.view.update()

    # ==========================================================================
    # visibility
    # ==========================================================================

    def toggle_faces(self, state):
        self.settings['faces.on'] = state == QtCore.Qt.Checked
        self.view.update()

    def toggle_edges(self, state):
        self.settings['edges.on'] = state == QtCore.Qt.Checked
        self.view.update()

    def toggle_vertices(self, state):
        self.settings['vertices.on'] = state == QtCore.Qt.Checked
        self.view.update()

    def toggle_normals(self, state):
        self.settings['normals.on'] = state == QtCore.Qt.Checked
        self.view.update()

    # ==========================================================================
    # color
    # ==========================================================================

    def change_vertices_color(self, color):
        self.settings['vertices.color'] = color
        self.view.update_vertex_buffer('vertices.color', self.view.array_vertices_color)
        self.view.update()
        self.app.main.activateWindow()

    def change_edges_color(self, color):
        self.settings['edges.color'] = color
        self.view.update_vertex_buffer('edges.color', self.view.array_edges_color)
        self.view.update()
        self.app.main.activateWindow()

    def change_faces_color_front(self, color):
        self.settings['faces.color:front'] = color
        self.view.update_vertex_buffer('faces.color:front', self.view.array_faces_color_front)
        self.view.update()
        self.app.main.activateWindow()

    def change_faces_color_back(self, color):
        self.settings['faces.color:back'] = color
        self.view.update_vertex_buffer('faces.color:back', self.view.array_faces_color_back)
        self.view.update()
        self.app.main.activateWindow()

    def change_normals_color(self, color):
        self.settings['normals.color'] = color
        self.view.update_vertex_buffer('normals.color', self.view.array_normals_color)
        self.view.update()
        self.app.main.activateWindow()

    # ==========================================================================
    # tools
    # ==========================================================================

    # open dialog or panel for additional options
    # set options and apply

    def flip_normals(self):
        mesh_flip_cycles(self.mesh)
        self.view.update_index_buffer('faces:front', self.view.array_faces_front)
        self.view.update_index_buffer('faces:back', self.view.array_faces_back)
        self.view.update()

    def subdivide(self, scheme, k):
        self.mesh = mesh_subdivide(self.mesh, scheme=scheme, k=k)
        self.view.make_buffers()
        self.view.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    config = {
        'menubar': [
            {
                'type'  : 'menu',
                'text'  : 'View',
                'items' : [
                    {
                        'type'  : 'menu',
                        'text'  : 'Set View',
                        'items' : [
                            {
                                'type'  : 'radio',
                                'items' : [
                                    {
                                        'text'    : 'Perspective',
                                        'action'  : 'set_view',
                                        'args'    : [View.VIEW_PERSPECTIVE, ],
                                        'checked' : True
                                    },
                                    {
                                        'text'    : 'Front',
                                        'action'  : 'set_view',
                                        'args'    : [View.VIEW_FRONT, ],
                                        'checked' : False
                                    },
                                    {
                                        'text'    : 'Left',
                                        'action'  : 'set_view',
                                        'args'    : [View.VIEW_LEFT, ],
                                        'checked' : False
                                    },
                                    {
                                        'text'    : 'Top',
                                        'action'  : 'set_view',
                                        'args'    : [View.VIEW_TOP, ],
                                        'checked' : False
                                    },
                                ]
                            }
                        ]
                    },
                    {'type' : 'separator'},
                    {'text' : 'Camera', 'action': 'update_camera_settings'},
                    {'type' : 'separator'},
                    {'text' : 'Capture Image', 'action': 'capture_image'},
                    {'text' : 'Capture Video', 'action': 'capture_video'},
                    {'type' : 'separator'}
                ]
            },
            {
                'type'  : 'menu',
                'text'  : 'Mesh',
                'items' : [
                    {'text' : 'From OBJ', 'action': 'from_obj'},
                    {'text' : 'From JSON', 'action': 'from_json'},
                    {'type' : 'separator'},
                    {'text' : 'To OBJ', 'action': 'to_obj'},
                    {'text' : 'To JSON', 'action': 'to_json'},
                    {'type' : 'separator'},
                    {
                        'type' : 'menu',
                        'text' : 'Polyhedrons',
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
                'text'  : 'Tools',
                'items' : [
                    {'text': 'Flip Normals', 'action': 'flip_normals'},
                    {'type': 'separator'},
                    {
                        'type'  : 'menu',
                        'text'  : 'Subdivision',
                        'items' : [
                            {'text': 'Catmull-Clark', 'action': 'subdivide', 'args': ['catmullclark', 1]}
                        ]
                    }
                ]
            },
            {
                'type'  : 'menu',
                'text'  : 'OpenGL',
                'items' : [
                    {'text' : 'Version Info', 'action': 'opengl_version_info'},
                    {'type' : 'separator'},
                    {
                        'type'  : 'radio',
                        'items' : [
                            {
                                'text'    : 'Version 2.1',
                                'action'  : 'opengl_set_version',
                                'args'    : [(2, 1), ],
                                'checked' : True
                            },
                            {
                                'text'    : 'Version 3.3',
                                'action'  : 'opengl_set_version',
                                'args'    : [(3, 3), ],
                                'checked' : False
                            },
                            {
                                'text'    : 'Version 4.1',
                                'action'  : 'opengl_set_version',
                                'args'    : [(4, 1), ],
                                'checked' : False
                            }
                        ]
                    },
                ]
            },
            {
                'type'  : 'menu',
                'text'  : 'Window',
                'items' : []
            },
            {
                'type'  : 'menu',
                'text'  : 'Help',
                'items' : []
            }
        ],
        'toolbar': [
            {'text': 'Zoom Extents', 'action': 'zoom_extents', 'image': 'icons/zoom/icons8-zoom-to-extents-50.png'},
            {'text': 'Zoom In', 'action': 'zoom_in', 'image': 'icons/zoom/icons8-zoom-in-50.png'},
            {'text': 'Zoom Out', 'action': 'zoom_out', 'image': 'icons/zoom/icons8-zoom-out-50.png'},
        ],
        'sidebar': [
            {
                'type'  : 'group',
                'text'  : None,
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
                    {
                        'type'  : 'group',
                        'text'  : None,
                        'items' : [
                            {'type' : 'checkbox', 'text' : 'normals', 'action' : 'toggle_normals', 'state' : False, },
                        ]
                    },
                ]
            },
            {
                'type' : 'group',
                'text' : None,
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

    style = """
QMainWindow {}

QMenuBar {}

QToolBar#Tools {
    padding: 4px;
}

QDockWidget#Sidebar {}

QDockWidget#Console {}

QDockWidget#Console QPlainTextEdit {
    background-color: #222222;
    color: #eeeeee;
    border-top: 8px solid #cccccc;
    border-left: 1px solid #cccccc;
    border-right: 1px solid #cccccc;
    border-bottom: 1px solid #cccccc;
    padding-left: 4px;
}
"""

    viewer = MeshViewer(config, style).show()
