
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.utilities import set_objects_show_names
from compas_blender.utilities import xdraw_lines


__all__ = [
    'EdgeArtist',
]


class EdgeArtist(object):

    __module__ = "compas_blender.artists.mixins"


    def clear_edges(self, keys=None):

        pass


    def clear_edgelabels(self):

        set_objects_show_names(objects=self.edge_objects, show=False)


    def draw_edges(self, width=0.05, keys=None, colors=None):

        self.clear_edges()
        self.clear_edgelabels()

        keys  = keys or list(self.datastructure.edges())
        lines = [0] * len(keys)

        if colors is None:
            colors = {key: self.defaults['color.line'] for key in keys}

        for c, (u, v) in enumerate(keys):
            lines[c] = {
                'start': self.datastructure.vertex_coordinates(u),
                'end':   self.datastructure.vertex_coordinates(v),
                'layer': self.layer,
                'color': colors[(u, v)],
                'width': width,
                'name':  'E{}-{}'.format(u, v),
            }

        self.edge_objects = xdraw_lines(lines=lines)


    def draw_edgelabels(self):

        set_objects_show_names(objects=self.edge_objects, show=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
