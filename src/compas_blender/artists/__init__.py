"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_blender.artists

Artists for visualising (painting) COMPAS data structures in Blender.
Artists convert COMPAS objects to Blender data and objects.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_blender.artists import MeshArtist

    mesh = Mesh.from_off(compas.get('tubemesh.off'))

    artist = MeshArtist(mesh)
    artist.draw()


Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:


Shape Artists
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/

    NetworkArtist
    MeshArtist


Robot Artists
=============

.. autosummary::
    :toctree: generated/

    RobotModelArtist


Base Classes
============

.. autosummary::
    :toctree: generated/

    Artist

"""

from ._artist import Artist  # noqa: F401

from .networkartist import *  # noqa: F401 F403
from .meshartist import *  # noqa: F401 F403
from .robotmodelartist import *  # noqa: F401 F403
# from .volmeshartist import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
