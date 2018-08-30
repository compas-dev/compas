from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import compas

from compas.geometry import centroid_points

from compas.viewers.viewer import Viewer

from compas.viewers.core.drawing import xdraw_polygons
from compas.viewers.core.drawing import xdraw_lines
from compas.viewers.core.drawing import xdraw_points


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MeshViewer']


class MeshViewer(Viewer):
    """"""

    def __init__(self, mesh, width=1440, height=900):
        super(MeshViewer, self).__init__(width=width, height=height)
        self.mesh = mesh
        self.center()

    # --------------------------------------------------------------------------
    # helpers (temp)
    # --------------------------------------------------------------------------

    def center(self):
        xyz = [self.mesh.vertex_coordinates(key) for key in self.mesh.vertices()]
        cx, cy, cz = centroid_points(xyz)
        for key, attr in self.mesh.vertices(True):
            attr['x'] -= cx
            attr['y'] -= cy

    # change this to a more flexible system
    # that provides similar possibilities as the network plotter
    def display(self):
        polygons = []
        for fkey in self.mesh.faces():
            points = self.mesh.face_coordinates(fkey)
            color_front = self.mesh.get_face_attribute(fkey, 'color', (0.8, 0.8, 0.8, 1.0))
            color_back  = (0.2, 0.2, 0.2, 1.0)
            polygons.append({'points': points,
                             'color.front': color_front,
                             'color.back' : color_back})

        lines = []
        for u, v in self.mesh.edges():
            lines.append({'start': self.mesh.vertex_coordinates(u),
                          'end'  : self.mesh.vertex_coordinates(v),
                          'color': (0.1, 0.1, 0.1),
                          'width': 1.})

        points = []
        for key in self.mesh.vertices():
            points.append({'pos'   : self.mesh.vertex_coordinates(key),
                           'color' : (0.4, 0.4, 0.4),
                           'size'  : 5.0})

        # normals = []
        # for fkey in self.mesh.faces():
        #     n  = self.mesh.face_normal(fkey, unitized=True)
        #     sp = self.mesh.face_centroid(fkey)
        #     ep = [sp[axis] + n[axis] for axis in (0, 1, 2)]
        #     normals.append({
        #         'start' : sp,
        #         'end'   : ep,
        #         'color' : (0.0, 1.0, 0.0),
        #         'width' : 2.0
        #     })

        xdraw_polygons(polygons)
        xdraw_lines(lines)
        xdraw_points(points)
        # xdraw_lines(normals)

    def keypress(self, key, x, y):
        """
        Assign mesh functionality to keys.

        The following keys have a mesh function assigned to them:
            * u: unify cycle directions
            * f: flip cycle directions
            * s: subdivide using quad subdivision
        """
        if key == 'u':
            self.mesh.unify_cycles()
            return
        if key == 'f':
            self.mesh.flip_cycles()
            return
        if key == 's':
            self.mesh.subdivide('quad')
            return
        if key == 'c':
            self.screenshot(os.path.join(compas.TEMP, 'screenshot.jpg'))
            return

    def special(self, key, x, y):
        """
        Assign mesh functionality to function keys.
        """
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh

    mesh = Mesh.from_polyhedron(6)

    viewer = MeshViewer(mesh, width=600, height=600)

    viewer.axes_on = False
    viewer.grid_on = False

    for i in range(10):
        viewer.camera.zoom_in()

    viewer.setup()
    viewer.show()
