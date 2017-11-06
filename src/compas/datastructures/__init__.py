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


mesh.operations
---------------

.. autosummary::
    :toctree: generated/

    mesh_collapse_edge
    mesh_split_edge
    mesh_split_face
    mesh_unweld_vertices


**The following operations are designed for triangle meshes.**

.. autosummary::
    :toctree: generated/

    trimesh_collapse_edge
    trimesh_split_edge
    trimesh_swap_edge


**The following operations are designed for triangle meshes.**

.. autosummary::
    :toctree: generated/

    trimesh_remesh
    trimesh_subdivide_loop


Network
=======

.. autosummary::
    :toctree: generated/

    Network
    FaceNetwork


network.operations
------------------

.. autosummary::
    :toctree: generated/

    network_split_edge


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
