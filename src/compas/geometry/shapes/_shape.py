from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
from compas.geometry import Primitive


__all__ = ['Shape']


class Shape(Primitive):
    """Base class for geometric shapes."""

    @abc.abstractmethod
    def to_vertices_and_faces(self):
        pass
