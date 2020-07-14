"""
********************************************************************************
objects
********************************************************************************

.. currentmodule:: compas_rhino.objects


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseObject


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshObject


"""
from __future__ import absolute_import

from .base import BaseObject
from .meshobject import MeshObject

from compas.datastructures import Mesh


BaseObject.register(Mesh, MeshObject)


__all__ = [name for name in dir() if not name.startswith('_')]
