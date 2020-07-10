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

    Object


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshObject


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .object import Object
from .meshobject import MeshObject

from compas.datastructures import Mesh


Object.register(Mesh, MeshObject)


__all__ = [name for name in dir() if not name.startswith('_')]
