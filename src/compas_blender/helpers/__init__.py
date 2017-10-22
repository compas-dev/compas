"""
.. _compas_blender.helpers:

********************************************************************************
helpers
********************************************************************************

.. module:: compas_blender.helpers


Helpers make it easier to work with datastructures in Blender.


mesh
====

.. autosummary::
    :toctree: generated/

    mesh_from_bmesh


network
=======

.. autosummary::
    :toctree: generated/

    network_from_bmesh


volmesh
=======

.. autosummary::
    :toctree: generated/


"""

from .mesh import *
from .network import *
from .volmesh import *
from .artists import *

from .mesh import __all__ as a
from .network import __all__ as b
from .volmesh import __all__ as c
from .artists import __all__ as d

__all__ = a + b + c + d
