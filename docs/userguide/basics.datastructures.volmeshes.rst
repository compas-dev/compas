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

Naked faces are faces without an opposite face, or with an opposite face that doesn"t belong to a cell.
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
>>> volmesh = VolMesh.from_obj("volmeshring.obj")

Equivalently, the geometry of a `VolMesh` can also be written to an OBJ file.
However, note that all additional data attributes (see :ref:`Vertex, Edges, Face, Cell Attributes`) are lost during this process.
Only the geometry survives this conversion process.

>>> volmesh.to_obj("volmeshring.obj")

Visualisation
=============

Like all other COMPAS geometry objects and data structures, volumetric meshes can be visualised by placing them in a scene.
For more information about visualisation with :class:`compas.scene.Scene`, see :doc:`/userguide/basics.visualisation`.
The snippet below uses `volmesh.obj`, which is available here: :download:`volmeshring.obj`.

>>> from compas.datastructures import VolMesh
>>> from compas.scene import Scene
>>> mesh = Mesh.from_obj("volmeshring.obj")
>>> scene = Scene()
>>> scene.add(mesh)
>>> scene.show()

.. figure:: /_images/userguide/basics.datastructures.volmeshes.volmeshring.png

Vertices, Edges, Faces, Cells
=============================

A `VolMesh` can only be constructed by providing information about the vertices and cells.
Edges are created implicitly, and can only exist as part of the topology of a cell.
Faces are not stored explicitly, but are generated automatically based on the corresponding (pairs of) halffaces.

Vertices, faces, and cells are identified by unique, positive and increasing integers.
Edges are identified by pairs of vertex identifiers.

In this section, we will use a `VolMesh` constructed from a mesh grid,
because its highly structured nature allows for easy and transparent counting and verification.

>>> volmesh = VolMesh.from_meshgrid(dx=3, nx=3)

.. figure:: /_images/userguide/basics.datastructures.volmeshes.volmeshgrid_3x3.png

>>> volmesh.number_of_vertices()
64
>>> volmesh.number_of_edges()
144
>>> volmesh.number_of_faces()
108
>>> volmesh.number_of_cells()
27

To iterate over vertices, edges, faces, and cells the `VolMesh` provides corresponding generators.

>>> volmesh.vertices()
<generator object VolMesh.vertices at ...>
>>> volmesh.edges()
<generator object VolMesh.edges at ...>
>>> volmesh.faces()
<generator object VolMesh.faces at ...>
>>> volmesh.cells()
<generator object VolMesh.cells at ...>

These generators are meant to be used in loops.

>>> for vertex in volmesh.vertices():
...     print(vertex)
...
0
1
2
3
4
# etc.

>>> for edge in volmesh.edges():
...     print(edge)
(0, 1)
(0, 4)
(0, 16)
(1, 2)
(1, 5)
# etc.

The edges are not stored explicitly in the data structure,
but instead generated automatically from the adjacency information of the vertices.
They are generated following the order of the vertex identifiers to make sure the order of edges is deterministic.

>>> for face in volmesh.faces():
...     print(face)
0
1
2
3
4
# etc

>>> for cell in volmesh.cells():
...     print(cell)
0
1
2
3
4
# etc

Lists of vertices, edges, faces, and cells have to be constructed explicitly.

>>> vertices = list(volmesh.vertices())
>>> vertices
[0, 1, 2, 3, 4, ..., 63]

>>> edges = list(volmesh.edges())
>>> edges
[(0, 1), (0, 4), (0, 16), (1, 2), (1, 5), ..., (62, 63)]

# NOTE: this is not ideal.

>>> faces = list(volmesh.faces())
>>> faces
[???]

>>> cells = list(volmesh.cells())
>>> cells
[0, 1, 2, 3, 4, ..., 27]

Vertex, Edge, Face, Cell Attributes
===================================

Arbitrary data can be assigned to vertices, edges, faces, and cells as vertex/edge/face/cell attributes, and to the overall `VolMesh` itself.
To allow for serialisatin of the `VolMesh` and all the data associated with it, the data should be JSON serialisable.
See :ref:`Data Serialisation` for more information.

The functionality is demonstrated here using vertex attributes.
The mechanism is exactly the same for edges, faces, and cells.

It is good practice to declare default values for the added data attributes.

>>> volmesh = VolMesh.from_meshgrid(dx=3, nx=10)
>>> volmesh.update_default_vertex_attributes(a=None, b=0.0, c=False)

Get the value of one attribute of one vertex.

>>> volmesh.vertex_attribute(vertex=0, name="a")
None

Get the value of multiple attributes of one vertex.

>>> volmesh.vertex_attributes(vertex=0, names=["a", "b"])
(None, 0.0)

Get the value of one attribute of all vertices.

>>> volmesh.vertices_attribute(name="a")
[None, None, None, ... None]

Get the value of multiple attributes of all vertices.

>>> volmesh.vertices_attributes(names=["b", "c"])
[(0.0, False), (0.0, False), (0.0, False), ..., (0.0, False)]

Similarly, for a selection of vertices.

>>> volmesh.vertices_attribute(name="b", vertices=[0, 1, 2, 3])
[0.0, 0.0, 0.0, 0.0]

>>> volmesh.vertices_attributes(names=["a", "c"], vertices=[0, 1, 2, 3])
[(None, False), (None, False), (None, False), (None, False)]

Updating attributes is currently only possible one vertex at a time.

>>> volmesh.vertex_attribute(vertex=0, name="a", value=(1.0, 0.0, 0.0))

>>> for vertex in volmesh.vertices():
...     if volmesh.vertex_degree(vertex) == 2:
...         volmesh.vertex_attribute(vertex=vertex, name="a", value=(1.0, 0.0, 0.0))
...

Overall Topology
================

More info coming...

* vertex_neighbors
* vertex_cells
* vertex_edges
* vertex_faces
* edge_cells
* edge_faces
* edge_halffaces
* cell_neighbors

Topology of a Cell
==================

Within the context of a cell, the topology of a `VolMesh` is the same as the topology of a regular `Mesh`.
Vertices are connected to other vertices, and faces to other faces, via edges.
An edge has two connected vertices, and at most two connected faces.
Each edge is split into two halfedges, one for each of the connected faces.

>>> volmesh = VolMesh.from_meshgrid(dx=3, nx=3)
>>> cell = volmesh.cell_sample(size=1).next()
>>> 

* cell_vertices
* cell_edges
* cell_halfedges
* cell_halffaces
* cell_faces
* cell_vertex_halffaces
* cell_vertex_faces
* cell_vertex_neighbors
* cell_edge_halffaces
* cell_edge_faces

.. edges and faces are implicit, and only used to store additional data
.. their identifiers are also implicit
.. halfedge_face
.. face_attributes
.. 

Geometry
========

* vertex_point
* edge_vector
* edge_line
* edge_start
* edge_end
* face_centroid
* face_area
* halfface_centroid
* halfface_polygon
* halfface_normal
* cell_volume
* cell_centroid
* cell_polyhedron

Filtering
=========

* vertices_where
* edges_where
* faces_where
* cells_where

Data Serialisation
==================

>>> volmesh.to_json("volmesh.json")
>>> volmesh = VolMesh.from_json("volmesh.json")

>>> s = volmesh.to_jsonstring()
>>> volmesh = VolMesh.from_jsonstring(s)

>>> session = {"volmesh": volmesh, "a": 1, "b": 2}
>>> compas.json_dump(session, "session.json")
>>> session = compas.json_load("session.json")
>>> volmesh = session["volmesh"]

Examples
========

.. literalinclude:: basics.datastructures.volmeshes_example-1.py
    :language: python

