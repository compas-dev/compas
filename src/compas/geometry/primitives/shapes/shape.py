from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.primitives import Primitive


__all__ = ['Shape']


class Shape(Primitive):
    """Base class for geometric shapes."""

    def __init__(self):
        super(Shape, self).__init__()

    def to_vertices_and_faces(self, **kwargs):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
