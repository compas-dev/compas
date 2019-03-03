
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.utilities import set_objects_show_names
from compas_blender.utilities import xdraw_points


__all__ = [
    'VertexArtist',
]


class VertexArtist(object):

    __module__ = "compas_blender.artists.mixins"

    def clear_vertices(self, keys=None):
        pass

    def clear_vertexlabels(self):
        set_objects_show_names(objects=self.vertex_objects, show=False)

    def draw_vertices(self, radius=0.05, keys=None):
        self.clear_vertices()
        self.clear_vertexlabels()
        keys   = keys or list(self.datastructure.vertices())
        points = [0] * len(keys)
        for c, key in enumerate(keys):
            points[c] = {
                'pos'    : self.datastructure.vertex_coordinates(key),
                'layer'  : self.layer,
                'name'   : 'V{0}'.format(key),
                'radius' : radius
            }
        self.vertex_objects = xdraw_points(points=points)

    def draw_vertexlabels(self):
        set_objects_show_names(objects=self.vertex_objects, show=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
