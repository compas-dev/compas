from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ["BaseArtist"]


class BaseArtist(object):
    """Abstract base class for all GH artists.
    """

    def __init__(self):
        pass

    def draw(self):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
