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
from compas.viewers.core import GLView
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
    """"""

    def __init__(self, app):
        self.app = app
        self.mesh = None
        self.settings = {}
        self.settings['vertices.size'] = 0.01
        self.settings['edges.width'] = 0.01
        self.settings['vertices.color'] = '#000000'
        self.settings['edges.color'] = '#666666'
        self.settings['faces.color:front'] = '#eeeeee'
        self.settings['faces.color:back'] = '#eeeeee'
        self.settings['vertices.on'] = True
        self.settings['edges.on'] = True
        self.settings['faces.on'] = True
        self.settings['vertices_labels.on'] = False
        self.settings['edges_labels.on'] = False
        self.settings['faces_labels.on'] = False
        self.settings['vertices_normals.on'] = False
        self.settings['faces_normals.on'] = False

    @property
    def view(self):
        return self.app.view

    def from_obj(self):
        filename, _ = get_obj_file()
        if filename:
            self.mesh = Mesh.from_obj(filename)
            center_mesh(self.mesh)
            # create triangle/quad strip
            # create display list
            self.view.update()

    def from_json(self):
        filename, _ = get_json_file()
        if filename:
            self.mesh = Mesh.from_json(filename)
            center_mesh(self.mesh)
            self.view.update()

    def from_polyhedron(self):
        print('from polyhedron')

    def zoom_extents(self):
        print('zoom extents')

    def zoom_in(self):
        print('zoom in')

    def zoom_out(self):
        print('zoom out')


class View(GLView):
    """"""

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller

    @property
    def mesh(self):
        return self.controller.mesh

    @property
    def settings(self):
        return self.controller.settings

    # don't compute any of this here
    # precompute whenever there are changes
    def paint(self):
        mesh = self.mesh
        if not mesh:
            return
        settings = self.settings
        if not self.settings:
            return
        key_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
        if settings['faces.on']:
            faces = []
            r, g, b = hex_to_rgb(settings['faces.color:front'], normalize=True)
            front = r, g, b, 1.0
            r, g, b = hex_to_rgb(settings['faces.color:back'], normalize=True)
            back = r, g, b, 1.0
            for fkey in mesh.faces():
                faces.append({'points'      : mesh.face_coordinates(fkey),
                              'color.front' : front,
                              'color.back'  : back})
            xdraw_polygons(faces)
        # if settings['edges.on']:
        #     lines = []
        #     color = hex_to_rgb(settings['edges.color'], normalize=True)
        #     width = settings['edges.width']
        #     for u, v in mesh.edges():
        #         lines.append({'start' : key_xyz[u],
        #                       'end'   : key_xyz[v],
        #                       'color' : color,
        #                       'width' : width})
        #     xdraw_cylinders(lines)
        # if settings['vertices.on']:
        #     points = []
        #     color = hex_to_rgb(settings['vertices.color'], normalize=True)
        #     size = settings['vertices.size']
        #     for key in mesh.vertices():
        #         pos = key_xyz[key]
        #         points.append({'pos'   : pos,
        #                        'color' : color,
        #                        'size'  : size})
        #     xdraw_spheres(points)


class MeshViewer(App):
    """"""

    def __init__(self, width=1440, height=900):
        super(MeshViewer, self).__init__()
        self.controller = Front(self)
        self.setup(width, height)
        self.init()
        self.show()

    def show(self):
        self.statusbar.showMessage('Ready')
        self.main.show()
        self.main.raise_()
        self.start()

    def setup(self, w, h):
        self.main = QtWidgets.QMainWindow()
        self.main.setFixedSize(w, h)
        self.main.setGeometry(0, 0, w, h)
        self.view = View(self.controller)
        self.main.setCentralWidget(self.view)
        self.menubar = self.main.menuBar()
        self.statusbar = self.main.statusBar()
        # self.toolbar = self.main.addToolBar('Tools')
        # self.toolbar.setMovable(False)

    def init(self):
        self.init_menubar()
        # self.init_toolbar()
        # self.init_sidepanel_left()
        # self.init_sidepanel_right()

    def init_menubar(self):
        mesh_menu   = self.menubar.addMenu('&Mesh')
        tools_menu  = self.menubar.addMenu('&Tools')
        view_menu   = self.menubar.addMenu('&View')
        window_menu = self.menubar.addMenu('&Window')
        help_menu   = self.menubar.addMenu('&Help')
        # mesh actions
        mesh_menu.addAction('&From OBJ', self.controller.from_obj)
        mesh_menu.addAction('&From JSON', self.controller.from_json)
        mesh_menu.addAction('&From Polyhedron', self.controller.from_polyhedron)
        # view actions
        view_menu.addAction('&Show Grid')
        view_menu.addAction('&Show Axes')
        view_menu.addSeparator()

    # def init_toolbar(self):
    #     self.toolbar.addAction('zoom extents', self.controller.zoom_extents)
    #     self.toolbar.addAction('zoom in', self.controller.zoom_in)
    #     self.toolbar.addAction('zoom out', self.controller.zoom_out)

    # def init_sidepanel_left(self):
    #     pass

    # def init_sidepanel_right(self):
    #     pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    viewer = MeshViewer()
