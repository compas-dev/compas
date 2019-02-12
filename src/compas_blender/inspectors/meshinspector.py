
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = [
    'MeshInspector',
]


class MeshInspector(object):

    def __init__(self):

        pass


    def DrawForeground(self, e):

        raise NotImplementedError


    def inspect_vertex(self, key):

        raise NotImplementedError


    def inspect_edge(self, key):

        raise NotImplementedError


    def inspect_face(self, key):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
