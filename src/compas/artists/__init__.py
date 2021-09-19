"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas.artists

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Artist


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DataArtistNotRegistered

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .exceptions import DataArtistNotRegistered
from .artist import Artist

__all__ = [
    'DataArtistNotRegistered',
    'Artist',
]
