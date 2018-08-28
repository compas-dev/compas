from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import compas

from compas.viewers.viewer import Viewer

from compas.viewers.core.drawing import xdraw_polygons
from compas.viewers.core.drawing import xdraw_lines
from compas.viewers.core.drawing import xdraw_points


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MultiMeshViewer']


class MultiMeshViewer(Viewer):
    """"""

    def __init__(self, meshes, colors, width=1440, height=900):
        super(MultiMeshViewer, self).__init__(width=width, height=height)
        self.meshes = meshes
        self.colors = colors

    def display(self):
        for i in range(len(self.meshes)):
            mesh = self.meshes[i]

            polygons = []
            for fkey in mesh.faces():
                color_front = self.colors[i]
                color_back  = (0.2, 0.2, 0.2, 1.0)
                polygons.append({'points': mesh.face_coordinates(fkey),
                                 'color.front': color_front,
                                 'color.back': color_back})

            lines = []
            for u, v in mesh.wireframe():
                lines.append({'start': mesh.vertex_coordinates(u),
                              'end': mesh.vertex_coordinates(v),
                              'color': (0.1, 0.1, 0.1),
                              'width': 1.})

            xdraw_polygons(polygons)
            xdraw_lines(lines)

    def keypress(self, key, x, y):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
