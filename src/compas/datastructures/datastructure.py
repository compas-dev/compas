from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data


class Datastructure(Data):
    """Base class for all data structures."""

    def __init__(self, name=None, **kwargs):
        super(Datastructure, self).__init__(**kwargs)
        self.attributes = {"name": name or self.__class__.__name__}

    @property
    def name(self):
        return self.attributes.get("name") or self.__class__.__name__

    @name.setter
    def name(self, value):
        self.attributes["name"] = value
