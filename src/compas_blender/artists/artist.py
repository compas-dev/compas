
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'Artist',
]


class Artist(object):

    __module__ = "compas_blender.artists"

    def __init__(self, layer=None):

        pass


    @property
    def layer(self):

        raise NotImplementedError


    @layer.setter
    def layer(self, value):

        raise NotImplementedError


    def redraw(self, timeout=None):

        raise NotImplementedError


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
