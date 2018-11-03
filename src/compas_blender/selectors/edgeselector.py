
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'EdgeSelector',
]


class EdgeSelector(object):

    @staticmethod
    def select_edge(self, message="Select an edge."):

        raise NotImplementedError


    @staticmethod
    def select_edges(self, message="Select edges."):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
