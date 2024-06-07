********************************************************************************
Vol(umetric) Meshes
********************************************************************************

.. currentmodule:: compas.datastructures

.. rst-class:: lead

A :class:`compas.datastructures.VolMesh` uses a "halfface" data structure to represent the topology and geometry of a cellular mesh,
and to facilitate the application of topological and geometrical operations on it.
In addition, it provides a number of methods for storing arbitrary data on vertices, edges, faces, and cell, and on the overall mesh itself.

.. note::

    Please refer to the API for a complete overview of all functionality:

    * :class:`compas.datastructures.VolMesh`

General Properties
==================

A `VolMesh` consists of vertices, edges, faces, and cells.
Currenly, a `VolMesh` can only be constructed by providing information about the vertices and cells.
This means that edges and faces are created implicitly, and can only exist as part of the topology of a cell.

An edge connects exactly two vertices.
All edges of a valid `VolMesh` belong to at least one cell.

A face consists of three or vertices, which are ordered such that they form a closed cycle.
The faces of a cell form a closed mesh.
The structure of this mesh is equivalent to the structure of a halfedge mesh (:class:`compas.datastructures.Mesh`).
The cycle directions of the faces are such that the resulting normals point towards the interior of the cell.

Neighbouring cells share at least one face.
A face can be shared by at most two neighbouring cells.
The cycle directions of the faces through which two neighbouring cells are connected are exactly opposite.

Naked faces are faces without an opposite face, or with an opposite face that doesn't belong to a cell.
Cells with naked faces are considered to be on the boundary of the `VolMesh`.

An empty `VolMesh` is valid.
A `VolMesh` with only vertices, but no cells is also valid.

VolMesh Construction
====================

VolMeshes can be constructed in a number of ways:

* from scratch, by adding vertices and cells one by one,
* from geometric input,
* using a special constructor function, or
* from the data contained in a file.

.. note::

    During construction, the validity of the input is not verified.
    The `VolMesh` is created with the input that is provided.
    Wrong input means wrong result.

From Scratch
------------

The following snippet constructs a `VolMesh` with one cell in the form of a unit cube.
Note that the vertices of the faces are ordered such that the corresponding normal vectors point toward the interior of the cube.

>>> from compas.datastructures import VolMesh
>>> volmesh = VolMesh()

>>> a = volmesh.add_vertex(x=0, y=0, z=0)
>>> b = volmesh.add_vertex(x=1, y=0, z=0)
>>> c = volmesh.add_vertex(x=1, y=1, z=0)
>>> d = volmesh.add_vertex(x=0, y=1, z=0)
>>> e = volmesh.add_vertex(x=0, y=0, z=1)
>>> f = volmesh.add_vertex(x=1, y=0, z=1)
>>> g = volmesh.add_vertex(x=1, y=1, z=1)
>>> h = volmesh.add_vertex(x=0, y=1, z=1)

>>> faces = [[a, b, c, d], [e, h, g, f], [a, e, f, b], [b, f, g, c], [c, g, h, d], [a, d, h, e]]
>>> cell = volmesh.add_cell(faces)

Using Constructors
------------------

Constructing `VolMesh` objects "from scratch", as shown above, obviously quickly becomes rather tedious.
Therefore, the `VolMesh` class provides class methods that can be used to construct volumetric meshes
more easily from various types of common inputs.

* :meth:`VolMesh.from_vertices_and_cells`
* :meth:`VolMesh.from_meshgrid`
* :meth:`VolMesh.from_meshes`
* :meth:`VolMesh.from_polyhedrons`

>>> from compas.datastructures import VolMesh
>>> volmesh = VolMesh.from_obj("meshes.obj")

From Data in a File
-------------------

Currently only OBJ files containing closed meshes are supported.

* :meth:`VolMesh.from_obj`

>>> from compas.datastructures import VolMesh
>>> volmesh = VolMesh.from_obj("meshes.obj")

Visualisation
=============

Like all other COMPAS geometry objects and data structures, volumetric meshes can be visualised by placing them in a scene.
For more information about visualisation with :class:`compas.scene.Scene`, see :doc:`/userguide/basics.visualisation`.
The snippet below uses `meshes.obj`, which is available here: :download:`meshes.obj`.

>>> from compas.datastructures import VolMesh
>>> from compas.scene import Scene
>>> mesh = Mesh.from_obj("meshes.obj")
>>> scene = Scene()
>>> scene.add(mesh)
>>> scene.show()

.. figure:: /_images/userguide/basics.datastructures.meshes.tubemesh.png


Vertices, Edges, Faces, Cells
=============================

Vertex, Edge, Face, Cell Attributes
===================================

Overall Topology
================

Topology of a Cell
==================

Geometry
========

Filtering
=========

Data Serialisation
==================

Examples
========
