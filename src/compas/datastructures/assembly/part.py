from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .node import Node


class Part(Node):
    """Base class for assembly parts."""

    def __init__(self, name, **kwargs):
        super(Part, self).__init__(name=name, **kwargs)
        self.geometries = []
