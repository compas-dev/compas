# from abc import ABCMeta
# from abc import abstractmethod


# class ArtistInterface(object):
#     __metaclass__ = ABCMeta

#     # @abstractmethod
#     # def redraw(self):
#     #     pass

#     @abstractmethod
#     def clear_layer(self):
#         """Clear the main drawing layer."""
#         pass

#     @abstractmethod
#     def clear(self):
#         """Clear all items drawn by the artist, without clearing the main drawing layer."""
#         pass


# class ArtistMixinInterface(object):
#     __metaclass__ = ABCMeta


from .meshartist import *
from .networkartist import *
from .volmeshartist import *

from .meshartist import __all__ as a
from .networkartist import __all__ as b
from .volmeshartist import __all__ as c

__all__ = a + b + c
