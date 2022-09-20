from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data

__all__ = ["Datastructure"]


class Datastructure(Data):
    """Base class for all data structures."""

    def __init__(self):
        super(Datastructure, self).__init__()
