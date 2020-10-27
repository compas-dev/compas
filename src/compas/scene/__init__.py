"""
********************************************************************************
scene
********************************************************************************

.. currentmodule:: compas.scene


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseScene
    BaseObject
    BaseArtist

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .artist import BaseArtist  # noqa: F401 F403
from .object import BaseObject  # noqa: F401 F403
from .scene import BaseScene  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
