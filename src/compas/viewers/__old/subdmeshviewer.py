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


__all__ = ['SubdMeshViewer']


class SubdMeshViewer(Viewer):
    """Viewer for subdivision meshes.

    Parameters
    ----------
    mesh : Mesh
        The *control* mesh object.
    subdfunc :callable
        The subdivision algorithm/scheme.
    width : int
        Optional. Width of the viewport. Default is ``1440``.
    height : int
        Optional. Height of the viewport. Default is ``900``.

    Warning
    -------
    Not properly tested on meshes with a boundary.

    Example
    -------
    .. code-block:: python

        from functools import partial

        from compas.datastructures import Mesh
        from compas.topology import mesh_subdivide
        from compas.viewers import SubdMeshViewer

        subdivide = partial(mesh_subdivide, scheme='doosabin')

        mesh = Mesh.from_polyhedron(6)

        viewer = SubdMeshViewer(mesh, subdfunc=subdivide, width=600, height=600)

        viewer.axes_on = False
        viewer.grid_on = False

        for i in range(10):
            viewer.camera.zoom_in()

        viewer.setup()
        viewer.show()

    """

    def __init__(self, mesh, subdfunc, width=1440, height=900):
        super(SubdMeshViewer, self).__init__(width=width, height=height)
        self.mesh = mesh
        self.subdfunc = subdfunc
        self.subd = None

    def display(self):
        xyz = {key: self.mesh.vertex_coordinates(key) for key in self.mesh.vertices()}

        lines = []
        for u, v in self.mesh.wireframe():
            lines.append({'start' : xyz[u],
                          'end'   : xyz[v],
                          'color' : (0.1, 0.1, 0.1),
                          'width' : 1.})

        points = []
        for key in self.mesh.vertices():
            points.append({'pos'   : xyz[key],
                           'color' : (0.0, 1.0, 0.0),
                           'size'  : 10.0})

        xdraw_lines(lines)
        xdraw_points(points)

        if self.subd:
            xyz   = {key: self.subd.vertex_coordinates(key) for key in self.subd.vertices()}
            front = (0.7, 0.7, 0.7, 1.0)
            back  = (0.2, 0.2, 0.2, 1.0)

            poly  = []
            for fkey in self.subd.faces():
                poly.append({'points': self.subd.face_coordinates(fkey),
                             'color.front': front,
                             'color.back' : back})

            lines = []
            for u, v in self.subd.wireframe():
                lines.append({'start': xyz[u],
                              'end'  : xyz[v],
                              'color': (0.1, 0.1, 0.1),
                              'width': 1.})

            xdraw_polygons(poly)
            xdraw_lines(lines)

    def keypress(self, key, x, y):
        key = key.decode("utf-8")
        if key == '1':
            self.subd = self.subdfunc(self.mesh, k=1)
        if key == '2':
            self.subd = self.subdfunc(self.mesh, k=2)
        if key == '3':
            self.subd = self.subdfunc(self.mesh, k=3)
        if key == '4':
            self.subd = self.subdfunc(self.mesh, k=4)
        if key == '5':
            self.subd = self.subdfunc(self.mesh, k=5)
        if key == 'c':
            self.screenshot(os.path.join(compas.TEMP, 'screenshot.jpg'))

    def subdivide(self, k=1):
        self.subd = self.subdfunc(self.mesh, k=k)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from functools import partial

    from compas.datastructures import Mesh
    from compas.topology import mesh_subdivide

    subdivide = partial(mesh_subdivide, scheme='doosabin')

    mesh = Mesh.from_polyhedron(6)

    viewer = SubdMeshViewer(mesh, subdfunc=subdivide, width=600, height=600)

    viewer.axes_on = False
    viewer.grid_on = False

    for i in range(10):
        viewer.camera.zoom_in()

    viewer.setup()
    viewer.show()
