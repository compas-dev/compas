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

from compas.files import STLReader
from compas.files import parse_stl_data

from compas.datastructures import Mesh

from compas.geometry import centroid_points
from compas.utilities import hex_to_rgb
from compas.utilities import flatten
from compas.topology import mesh_flip_cycles
from compas.topology import mesh_subdivide

from compas.viewers import core
from compas.viewers.meshviewer.model import MeshView


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Controller', ]


get_obj_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select OBJ file',
    dir=compas.DATA,
    filter='OBJ files (*.obj)'
)

get_stl_file = partial(
    QtWidgets.QFileDialog.getOpenFileName,
    caption='Select STL file',
    dir=compas.DATA,
    filter='STL files (*.stl)'
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


class Controller(core.controller.Controller):

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
        super(Controller, self).__init__(app)
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
            attr['z'] -= cz

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

    def to_obj(self):
        self.message('Export to OBJ is under construction...')

    def from_json(self):
        filename, _ = get_json_file()
        if filename:
            self.mesh = Mesh.from_json(filename)
            self.center_mesh()
            self.view.make_buffers()
            self.view.update()

    def to_json(self):
        self.message('Export to JSON is under construction...')

    def from_stl(self):
        filename, _ = get_stl_file()
        if filename:
            reader = STLReader(filename)
            reader.read()
            vertices, faces = parse_stl_data(reader.facets)
            self.mesh = Mesh.from_vertices_and_faces(vertices, faces)
            self.center_mesh()
            self.view.make_buffers()
            self.view.update()

    def to_stl(self):
        self.message('Export to STL is under construction...')

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

    pass
