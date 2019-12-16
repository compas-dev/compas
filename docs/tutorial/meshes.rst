********************************************************************************
Meshes
********************************************************************************

.. highlight:: python

COMPAS meshes are polygon meshes with support for n-sided polygonal
faces. the meshes are presented using a half-edge data structure. In a
half-edge data structure, each edge is composed of two half-edges with
opposite orientation. Each half-edge is part of exactly one face, unless
it is on the boundary. An edge is thus incident to at least one face and
at most to two. The half-edges of a face form a continuous cycle,
connecting the vertices of the face in a specific order forming a closed
n-sided polygon. The ordering of the vertices determines the direction
of its normal.

Check out the docs for detailed information about the mesh and the available
functionality: :class:`compas.datastructures.Mesh`.


Making a mesh
=============

>>> from compas.datastructures import Mesh
>>> mesh = Mesh()


Adding vertices and faces
=========================

>>> a = mesh.add_vertex()
>>> b = mesh.add_vertex(x=1.0)
>>> c = mesh.add_vertex(x=1.0, y=1.0)
>>> d = mesh.add_vertex(y=1.0)

>>> f = mesh.add_face([a, b, c, d])


.. note::

    Edges cannot be added explicitly. They are added automatically when
    faces are added.


Identifiers
===========

All vertices of a mesh have a unique ID, the "key" of the vertex. By
default, keys are integers, and every vertex is assigned a number
corresponding to the order in which it is added. The number is always
the highest number used so far, plus one.

>>> print(a, type(a))
0 <class 'int'>

>>> b == a + 1
True


IDs can also be assigned explicitly, as integers or as any other *hashable*
type.

Faces are also assigned a unique id. As with vertices, keys are integers
by default, but any other *hashable* type can be assigned explicitly.

.. code-block:: python

    >>> print(f, type(f))
    0 <class 'int'>


Constructors
============

Meshes can be constructed from data contained in files. Currently, the
following formats are supported: ``obj``, ``ply``, ``stl``.

.. code-block:: python

    >>> mesh = Mesh.from_obj('faces.obj')
    >>> mesh = Mesh.from_ply('bunny.ply')
    >>> mesh = Mesh.from_stl('cube.stl')


COMPAS provides a set of sample files that can be used during development,
or simply to make examples like the ones in this tutorial.

.. code-block:: python

    >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
    >>> mesh = Mesh.from_ply(compas.get('bunny.ply'))
    >>> mesh = Mesh.from_stl(compas.get('cube.stl'))


Data
====

All data accessors return objects that are meant to be iterated over
(dictionary key iterators or generator objects). Storing the data in
lists that can be reused multiple times must be done explicitly.


Iteration
---------

.. code-block:: python

    >>> mesh.vertices()
    <dict_keyiterator at 0x60d74f278>

.. code-block:: python

    >>> for key in mesh.vertices():
    ...     print(key)
    ...
    0
    1
    2
    3
    ...
    32
    33
    34
    35

.. code-block:: python

    >>> mesh.faces()
    <generator object Mesh.faces at 0x60d723e08>

.. code-block:: python

    >>> for key in mesh.faces():
    ...     print(key)
    ...
    0
    1
    2
    3
    ...
    21
    22
    23
    24

.. code-block:: python

    >>> mesh.edges()
    <generator object Mesh.edges at 0x60d723a98>

.. code-block:: python

    >>> for key in mesh.edges():
    ...     print(key)
    ...
    (0, 1)
    (0, 6)
    (1, 7)
    (1, 2)
    ...
    (31, 32)
    (32, 33)
    (33, 34)
    (34, 35)

Lists
-----

.. code-block:: python

    >>> list(mesh.vertices())
    [0, 1, 2, 3, ... 32, 33, 34, 35]

.. code-block:: python

    >>> list(mesh.faces())
    [0, 1, 2, 3, ... 21, 22, 23, 24]

.. code-block:: python

    >>> list(mesh.edges())
    [(0, 1), (0, 6), (1, 7), (1, 2), ... (31, 32), (32, 33), (33, 34), (34, 35)]


Attributes
==========

All vertices, faces, and edges automatically have the default attributes
specified by the mesh class. The default vertex attributes are xyz
coordinates, with ``x=0``, ``y=0``, and ``z=0``. Edges and faces have no
default attributes.

To change the default attributes, do:

.. code-block:: python

    >>> mesh.update_default_vertex_attributes(z=10, is_fixed=False)
    >>> mesh.update_default_face_attributes(is_loaded=True)
    >>> mesh.update_default_edge_attributes(q=1.0)


Getting attributes
------------------

.. code-block:: python

    >>> mesh.get_vertex_attribute(mesh.get_any_vertex(), 'x')
    2.0

.. code-block:: python

    >>> mesh.get_vertices_attribute('x')
    [0.0, 2.0, 4.0, 6.0, ... 4.0, 6.0, 8.0, 10.0]

.. code-block:: python

    >>> mesh.get_vertices_attributes('xyz')
    [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [4.0, 0.0, 0.0], [6.0, 0.0, 0.0],
    ...
    [4.0, 10.0, 0.0], [6.0, 10.0, 0.0], [8.0, 10.0, 0.0], [10.0, 10.0, 0.0]]


Setting attributes
------------------

.. code-block:: python

    >>> mesh.set_vertex_attribute(0, 'is_fixed', True)
    >>> mesh.set_vertex_attributes(0, ('is_fixed', 'z'), (False, 10))
    >>> mesh.set_vertices_attribute('z', 10)
    >>> mesh.set_vertices_attributes(('z', 'is_fixed'), (0, False))


Connectivity
============

.. code-block:: python

    >>> for key in mesh.vertices():
    ...     print(key, "(neighbors)", mesh.vertex_neighbors(key, ordered=True))
    ...     print(key, "(faces)", mesh.vertex_faces(key, ordered=True))
    ...
    0 (neighbors) [6, 1]
    0 (faces) [0]
    1 (neighbors) [0, 7, 2]
    1 (faces) [0, 1]
    2 (neighbors) [1, 8, 3]
    2 (faces) [1, 2]
    3 (neighbors) [2, 9, 4]
    3 (faces) [2, 3]
    ...
    32 (neighbors) [33, 26, 31]
    32 (faces) [22, 21]
    33 (neighbors) [34, 27, 32]
    33 (faces) [23, 22]
    34 (neighbors) [35, 28, 33]
    34 (faces) [24, 23]
    35 (neighbors) [29, 34]
    35 (faces) [24]


.. code-block:: python

    >>> for fkey in mesh.faces():
    ...     print(fkey, "(vertices)", mesh.face_vertices(fkey))
    ...     print(fkey, "(half-edges)", mesh.face_halfedges(fkey))
    ...     print(fkey, "(neighbors)", mesh.face_neighbors(fkey))
    ...
    0 (vertices) [0, 1, 7, 6]
    0 (half-edges) [(0, 1), (1, 7), (7, 6), (6, 0)]
    0 (neighbors) [1, 5]
    1 (vertices) [1, 2, 8, 7]
    1 (half-edges) [(1, 2), (2, 8), (8, 7), (7, 1)]
    1 (neighbors) [2, 6, 0]
    2 (vertices) [2, 3, 9, 8]
    2 (half-edges) [(2, 3), (3, 9), (9, 8), (8, 2)]
    2 (neighbors) [3, 7, 1]
    3 (vertices) [3, 4, 10, 9]
    3 (half-edges) [(3, 4), (4, 10), (10, 9), (9, 3)]
    3 (neighbors) [4, 8, 2]
    ...
    21 (vertices) [25, 26, 32, 31]
    21 (half-edges) [(25, 26), (26, 32), (32, 31), (31, 25)]
    21 (neighbors) [16, 22, 20]
    22 (vertices) [26, 27, 33, 32]
    22 (half-edges) [(26, 27), (27, 33), (33, 32), (32, 26)]
    22 (neighbors) [17, 23, 21]
    23 (vertices) [27, 28, 34, 33]
    23 (half-edges) [(27, 28), (28, 34), (34, 33), (33, 27)]
    23 (neighbors) [18, 24, 22]
    24 (vertices) [28, 29, 35, 34]
    24 (half-edges) [(28, 29), (29, 35), (35, 34), (34, 28)]
    24 (neighbors) [19, 23]


Geometry
========

There are many functions for inspecting the geometry of the mesh.

* ``Mesh.vertex_coordinates``
* ``Mesh.vertex_normal``
* ``Mesh.vertex_laplacian``
* ``Mesh.edge_length``
* ``Mesh.edge_point``
* ``Mesh.edge_vector``
* ``Mesh.edge_direction``
* ``Mesh.face_centroid``
* ``Mesh.face_normal``
* ``Mesh.face_plane``
* ``Mesh.face_frame``
* ``Mesh.face_area``


Serialisation
=============

A COMPAS mesh can be converted to a data dict that contains
all the information required to recreate an instance of the
type class:`compas.datastructures.Mesh` without loss of information.


.. code-block:: python

    >>> data = mesh.to_data()
    >>> mesh = Mesh.from_data(data)


This data can be serialised to various formats such that
it can be stored in a file and saved for later use.


Json
----

The ``JSON`` format is used by :mod:`compas.rpc` and :mod:`compas.remote`,
which is still under construction, to send data back and forth
between a client and a remote service.

In case of :class:`compas.utilities.XFunc`, ``JSON`` is used to comunicate
with a CPython subprocess.

.. code-block:: python

    >>> mesh.to_json('mesh.json')
    >>> mesh = Mesh.from_json('mesh.json')


Pickle
------

.. code-block:: python

    >>> mesh.dump('mesh.pickle')
    >>> mesh.load('mesh.pickle')
    >>> s = mesh.dumps()
    >>> mesh.loads(s)


Visualisation
=============

.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas_plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in mesh.vertices_on_boundary()},
        radius={key: 0.2 for key in mesh.vertices_on_boundary()},
        text={key: str(key) for key in mesh.vertices_on_boundary()})

    plotter.draw_edges(
        color={key: '#ff0000' for key in mesh.edges_on_boundary()},
        width={key: 3 for key in mesh.edges_on_boundary()})

    plotter.draw_faces(
        text={key: str(key) for key in mesh.faces_on_boundary()})

    plotter.show()
