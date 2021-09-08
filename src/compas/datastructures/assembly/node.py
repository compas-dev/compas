from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Datastructure


class Node(Datastructure):
    """Base class for the components of an assembly."""

    def __init__(self, name=None, **kwargs):
        super(self, Node).__init__(name=name, **kwargs)
        self.attributes = {}
