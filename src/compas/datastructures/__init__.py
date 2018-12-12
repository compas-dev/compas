"""
********************************************************************************
compas.datastructures
********************************************************************************

.. currentmodule:: compas.datastructures


Mesh
====

The mesh is implemented as a half-edge datastructure.
It is meant for the representation of polygonal *"surface"* meshes. A mesh can be
connected or disconnected. A mesh can be closed or open. A mesh can be comprised
of only vertices.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Mesh


Network
=======

The network is a connectivity graph.
It is meant for the representation of networks of vertices connected by edges.
The edges are directed. A network does not have faces. A network can be connected
or disconnected. A network with vertices only is also a valid network.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Network


VolMesh
=======

The volmesh is a cellular mesh. It is implemented as
a half-plane, the three-dimensional equivalent of a half-edge. It can, for example,
be used for the representation of subdivided/partitioned polyhedra.


.. autosummary::
    :toctree: generated/
    :nosignatures:

    VolMesh

"""

from __future__ import absolute_import, division, print_function


class Datastructure(object):
    pass


from .network import *
from .mesh import *
from .volmesh import *

__all__ = [name for name in dir() if not name.startswith('_')]
