from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


__all__ = ["BaseArtist"]


class BaseArtist(ABC):
    """Abstract base class for all GH artists.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
