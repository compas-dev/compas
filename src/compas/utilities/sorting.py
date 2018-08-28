from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__author__    = ['Tom Van Mele']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


def bubble(items):
    for n in range(len(items) - 1, 0, -1):
        for i in range(n):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
