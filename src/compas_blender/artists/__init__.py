"""
********************************************************************************
compas_blender.artists
********************************************************************************

.. currentmodule:: compas_blender.artists

Artists for visualising (painting) COMPAS data structures in Blender.


.. autosummary::
    :toctree: generated/

    MeshArtist
    NetworkArtist
    VolMeshArtist

"""

from .artist import *  # noqa: F401 F403
from .meshartist import *  # noqa: F401 F403
from .networkartist import *  # noqa: F401 F403
from .volmeshartist import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
