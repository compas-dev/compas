from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

__all__ = ['Collection']


class Collection(object):

    __slots__ = ['_items']

    def transform(self, X):
        raise NotImplementedError

    def transformed(self, X):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
