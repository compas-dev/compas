from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})
# https://stackoverflow.com/questions/35673474/using-abc-abcmeta-in-a-way-it-is-compatible-both-with-python-2-7-and-python-3-5


__all__ = ['Base']


class Base(ABC):
    """Abstract base class for all COMPAS objects.

    Attributes
    ----------
    data : dict
        The fundamental data describing the object.
        The structure of the data dict is defined by the implementing classes.

    """

    @abc.abstractproperty
    def data(self):
        pass

    @data.setter
    def data(self, data):
        pass

    @abc.abstractclassmethod
    def from_data(cls, data):
        pass

    @abc.abstractmethod
    def to_data(self):
        pass

    @abc.abstractclassmethod
    def from_json(cls, filepath):
        pass

    @abc.abstractmethod
    def to_json(self, filepath):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
