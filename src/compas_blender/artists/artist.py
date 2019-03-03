
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import bpy
except ImportError:
    pass


__all__ = [
    'Artist',
]


class Artist(object):

    __module__ = "compas_blender.artists"

    def __init__(self, layer=None):

        self.layer = layer
        self.defaults = {
            'color.point':   [255, 255, 255],
            'color.line':    [0, 0, 0],
            'color.polygon': [210, 210, 210],
        }
        self.vertex_objects = []
        self.edge_objects   = []
        self.face_objects   = []

    def redraw(self, timeout=None):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def clear_layer(self):
        raise NotImplementedError


    def save(self, path, width=1920, height=1080, scale=1,
             draw_grid=False, draw_world_axes=False, draw_cplane_axes=False, background=False):
        raise NotImplementedError


    def draw_points(self, points, layer=None, clear_layer=False, redraw=False):
        raise NotImplementedError

    def draw_lines(self, lines, layer=None, clear_layer=False, redraw=False):
        raise NotImplementedError

    def draw_polygons(self, polygons, layer=None, clear_layer=False, redraw=False):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
