"""
.. _compas.datastructures:

********************************************************************************
datastructures
********************************************************************************

.. module:: compas.datastructures


Mesh
====

Package for working with mesh objects.

.. autosummary::
    :toctree: generated/

    Mesh

Network
=======

.. autosummary::
    :toctree: generated/

    Network
    FaceNetwork


VolMesh
=======

*Under constuction...*

.. autosummary::
    :toctree: generated/

    VolMesh


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
