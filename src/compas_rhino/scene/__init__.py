"""
******************
scene
******************

.. currentmodule:: compas_rhino.scene

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Scene

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxObject
    CapsuleObject
    ConeObject
    CylinderObject
    PolyhedronObject
    SphereObject
    TorusObject

.. autosummary::
    :toctree: generated/
    :nosignatures:

    NetworkObject
    MeshObject
    VolMeshObject

"""
from __future__ import absolute_import

import compas_rhino.artists  # noqa: F401
from . import objects  # noqa: F401
from .objects import Object
from .objects import BoxObject
from .objects import CapsuleObject
from .objects import ConeObject
from .objects import CylinderObject
from .objects import PolyhedronObject
from .objects import SphereObject
from .objects import TorusObject
from .objects import NetworkObject
from .objects import MeshObject
from .objects import VolMeshObject

from .scene import Scene

__all__ = [
    'Scene',

    'Object',
    'BoxObject',
    'CapsuleObject',
    'ConeObject',
    'CylinderObject',
    'PolyhedronObject',
    'SphereObject',
    'TorusObject',
    'MeshObject',
    'NetworkObject',
    'VolMeshObject',
]
