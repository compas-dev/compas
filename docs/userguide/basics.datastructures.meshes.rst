********************************************************************************
Meshes
********************************************************************************

.. rst-class:: lead

A :class:`compas.datastructures.Mesh` uses a halfedge data structure to represent the topology and geometry of a polygonal mesh,
and to facilitate the application of topological and geometrical operations on it.
In addition, it provides a number of methods for storing arbitrary data on vertices, edges and faces, and the overall mesh itself.

.. note::

    Please refer to the API for a complete overview of all functionality:

    * :class:`compas.datastructures.HalfEdge`
    * :class:`compas.datastructures.Mesh`


Mesh Construction
=================

Meshes can be constructed in a number of ways:

* from scratch, by adding vertices and faces one by one,
* using a special constructor function, or
* from the data contained in a file.

From Scratch
------------

>>> from compas.datastructures import Mesh
>>> mesh = Mesh()
>>> a = mesh.add_vertex(x=0, y=0, z=0)
>>> b = mesh.add_vertex(x=1, y=0, z=0)
>>> c = mesh.add_vertex(x=1, y=1, z=0)
>>> d = mesh.add_vertex(x=0, y=1, z=0)
>>> face = mesh.add_face([a, b, c, d])
>>> mesh
<Mesh with 4 vertices and 1 faces>

Using Constructors
------------------

>>> from compas.datastructures import Mesh
>>> mesh = Mesh.from_lines(...)
>>> mesh = Mesh.from_meshgrid(...)
>>> mesh = Mesh.from_polygons(...)
>>> mesh = Mesh.from_polyhedron(...)
>>> mesh = Mesh.from_shape(...)
>>> mesh = Mesh.from_vertices_and_faces(...)

From Data in a File
-------------------

>>> from compas.datastructures import Mesh
>>> mesh = Mesh.from_obj('mesh.obj')
>>> mesh = Mesh.from_off('mesh.off')
>>> mesh = Mesh.from_ply('mesh.ply')
>>> mesh = Mesh.from_stl('mesh.stl')


Visualisation
=============

Like all other COMPAS geometry objects and data structures, meshes can be visualised by placing them in a scene.
For more information about visualisation with :class:`compas.scene.Scene`, see :doc:`/userguide/basics.visualisation`.

>>> from compas.datastructures import Mesh
>>> from compas.scene import Scene
>>> mesh = Mesh.from_obj(compas.get('tubemesh.obj'))
>>> scene = Scene()
>>> scene.add(mesh)
>>> scene.show()

.. figure:: /_images/userguide/basics.datastructures.meshes.tubemesh.png


Vertices, Edges, Faces
======================

A mesh has vertices, edges, and faces.
Vertices are identified by a positive integer that is unique among the vertices of the current mesh.
Faces are identified by a positive integer that is unique among the faces of the current mesh.
Edges are identified by a pair (tuple) of two vertex identifiers.

>>> mesh = Mesh.from_meshgrid(dx=10, dy=10, nx=10, ny=10)
>>> mesh.number_of_vertices()
121
>>> mesh.number_of_edges()
200
>>> mesh.number_of_faces()
81

Vertex, edge, and face accessors are generators: they are meant to be used in loops.

>>> mesh.vertices()
<generator object Mesh.vertices at ...>
>>> mesh.edges()
<generator object Mesh.edges at ...>
>>> mesh.faces()
<generator object Mesh.faces at ...>

>>> for vertex in mesh.vertices():
...     # do something with this vertex
...     print(vertex)
...
0
1
2
...

>>> for edge in mesh.edges():
...     # do something with this edge
...     print(edge)
...
(0, 1)
(1, 2)
(2, 3)
...

>>> for face in mesh.faces():
...     # do something with this face
...     print(face)
...
0
1
2
...

Lists of vertices, edges, and faces have to be constructed explicitly.

>>> vertices = list(mesh.vertices())
>>> vertices
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ..., 120]

>>> edges = list(mesh.edges())
>>> edges
[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), ..., (115, 120)]

>>> faces = list(mesh.faces())
>>> faces
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ..., 80]


Halfedge Data Structure
=======================

The topology of a mesh is stored in a halfedge data structure.
In this data structure, vertices are connected to other vertices, and faces to other faces via edges.
An edge has at most two connected faces.
Each each is split into two halfedges, one for each of the connected faces.
If an edge has only one connected face, the edge is on the boundary.

Note that in a mesh constructed using :meth:`compas.datastructures.Mesh.from_meshgrid`, the vertices are organised in a specific way.
We will use that structure to explain some of the topological concepts more easily.

>>> mesh = Mesh.from_meshgrid(dx=9, nx=9)

>>> for i in range(0, 10):
>>>     print(mesh.is_vertex_on_boundary(i))
...
True
True
True
True
True
True
True
True
True
True

.. figure:: /_images/userguide/basics.datastructures.meshes.meshgrid-column0.png


>>> for i in range(30, 40):
>>>     print(mesh.is_vertex_on_boundary(i))
...
True
False
False
False
False
False
False
False
False
True

.. figure:: /_images/userguide/basics.datastructures.meshes.meshgrid-column3.png


Mesh Geometry
=============

Data Attributes
===============

Additional data can be assigned to vertices, edges, and faces, as vertex/edge/face attributes, and to the overall mesh itself.

>>> mesh = Mesh.from_meshgrid(dx=10, dy=10, nx=10, ny=10)

It is recommended to register default values for the vertex, edge and face attributes.

>>> mesh.update_default_vertex_attributes(is_fixed=False)
>>> mesh.update_default_edge_attributes(weight=1.0)
>>> mesh.update_default_face_attributes(color=None)

Attributes can be accessed per element, per group of elements, or for all elements at once.

>>> mesh.vertex_attribute(0, 'is_fixed')
False
>>> mesh.vertices_attribute('is_fixed', vertices=[])

>>> mesh.vertices_attribute(vertices=mesh.vertices_where(vertex_degree=2), is_anchor=True)
>>> mesh.edges_attribute(edges=mesh.edges_on_boundary(), weight=10.0)

>>> 


Filtering
=========




Mesh Serialisation
==================

>>> mesh.to_json('mesh.json')
>>> mesh = Mesh.from_json('mesh.json')

>>> s = mesh.to_jsonstring()
>>> mesh = Mesh.from_jsonstring(s)

>>> session = {}


A Simple Example
================
