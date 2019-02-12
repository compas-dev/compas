
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = [
    'VertexModifier'
]


class VertexModifier(object):

    @staticmethod
    def move_vertex(self, key, constraint=None, allow_off=None):

        raise NotImplementedError


    @staticmethod
    def move_vertices(self, keys):

        raise NotImplementedError


    @staticmethod
    def update_vertex_attributes(self, keys, names=None):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
