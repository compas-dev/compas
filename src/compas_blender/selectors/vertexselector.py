
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'VertexSelector',
]


class VertexSelector(object):

    @staticmethod
    def select_vertex(self, message="Select a vertex."):

        raise NotImplementedError


    @staticmethod
    def select_vertices(self, message="Select vertices."):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
