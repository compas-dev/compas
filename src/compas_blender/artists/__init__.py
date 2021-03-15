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

from ._artist import BaseArtist

from .networkartist import NetworkArtist
from .meshartist import MeshArtist
from .robotmodelartist import BaseRobotModelArtist, RobotModelArtist


__all__ = [
    'BaseArtist', 'NetworkArtist', 'MeshArtist', 'BaseRobotModelArtist', 'RobotModelArtist'
]
