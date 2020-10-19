from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
from compas.geometry import Primitive


__all__ = ['Shape']


class Shape(Primitive):
    """Base class for geometric shapes."""

    def __init__(self):
        super(Shape, self).__init__()

    @abc.abstractmethod
    def to_vertices_and_faces(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
