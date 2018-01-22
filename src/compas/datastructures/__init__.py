"""
********************************************************************************
datastructures
********************************************************************************

.. module:: compas.datastructures

This package defines a mesh datastructure, a network, and a cellular mesh.


Mesh
====

The mesh is implemented as a half-edge datastructure.
It is meant for the representation of polygonal *"surface"* meshes. A mesh can be
connected or disconnected. A mesh can be closed or open. A mesh can be comprised
of only vertices.

.. unified face orientation => consistent/compatible cycle directions
.. vertex => neighbours => halfedges => faces (optionally ordered around vertex)
.. face => vertices => halfedges => neighbours
.. vertex => connectivity, area, normal, laplacian, ...
.. face => area, normal, ...

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

.. vertex => neighbours, laplacian
.. edge =>

.. form := network => ordering of neighbours is enough to construct dual
.. force := mesh => with faces constructed from the ordering ov neighbours

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


.. Assembly
.. ========

.. .. autosummary::
..     :toctree: generated/
..     :nosignatures:

..     Assembly

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
