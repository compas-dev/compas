
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = [
    'EdgeModifier'
]


class EdgeModifier(object):

    @staticmethod
    def move_edge(self, key, constraint=None, allow_off=None):

        raise NotImplementedError


    @staticmethod
    def update_edge_attributes(self, keys, names=None):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
