"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_blender.artists

Artists for visualising (painting) COMPAS data structures in Blender.


Base Classes
============

.. autosummary::
    :toctree: generated/

    BaseArtist


Classes
=======

.. autosummary::
    :toctree: generated/

    NetworkArtist
    MeshArtist
    RobotModelArtist

"""

from ._artist import *  # noqa: F401 F403

from .networkartist import *  # noqa: F401 F403
from .meshartist import *  # noqa: F401 F403
from .robotmodelartist import *  # noqa: F401 F403
# from .volmeshartist import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
