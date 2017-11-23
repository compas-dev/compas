"""
.. _compas.datastructures:

********************************************************************************
datastructures
********************************************************************************

.. module:: compas.datastructures


.. autosummary::
    :toctree: generated/

    Mesh
    Network
    VolMesh

Mesh
====

Network
=======

VolMesh
=======


"""

from __future__ import print_function


class Datastructure(object):
    pass


from .network import *
from .mesh import *
from .volmesh import *

from .network import __all__ as a
from .mesh import __all__ as c
from .volmesh import __all__ as d

__all__ = a + c + d
