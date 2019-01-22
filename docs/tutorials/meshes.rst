********************************************************************************
Working with Meshes
********************************************************************************

**COMPAS** meshes are polygon meshes with support for n-sided polygonal
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

.. code:: ipython3

    import compas
    from compas.datastructures import Mesh
    
    mesh = Mesh()


Adding vertices and faces
=========================

.. code:: ipython3

    a = mesh.add_vertex()
    b = mesh.add_vertex(x=1.0)
    c = mesh.add_vertex(x=1.0, y=1.0)
    d = mesh.add_vertex(y=1.0)

.. code:: ipython3

    f = mesh.add_face([a, b, c, d])


.. note::

    Edges cannot be added explicitly. They are added automatically when
    faces are added.


Identifiers
===========

All vertices of a mesh have a unique id, the *key* of the vertex. By
default, keys are integers, and every vertex is assigned a unmbr
corresponding to the order in which they are added. The number is always
the highest number used so far, plus one.

Keys can be assigned explicitly, as integers or as any other *hashable*
type.

.. code:: ipython3

    print(a, type(a))


.. parsed-literal::

    0 <class 'int'>


.. code:: ipython3

    b == a + 1


.. parsed-literal::

    True


Faces are also assigned a unique id. As with vertices, keys are integers
by default, but any other *hashable* type can be assigned explicitly.

.. code:: ipython3

    print(f, type(f))


.. parsed-literal::

    0 <class 'int'>


Constructors
============

Meshes can be constructed from data contained in files. Currently, the
following formats are supported: ``obj``, ``ply``, ``stl``. **COMPAS**
provides a set of sample files that can be used to develop new
functionality, or simply to make examples like the ones in this
tutorial.

.. code:: ipython3

    mesh = Mesh.from_obj(compas.get('faces.obj'))


.. code:: ipython3

    # mesh = Mesh.from_ply(compas.get('bunny.ply'))
    # mesh = Mesh.from_stl(compas.get('cube.stl'))


Data
====

All data accessors return objects that are meant to be iterated over
(dictionary key iterators or generator objects). Storing the data in
lists that can be reused multiple times must be done explicitly.


Iteration
---------

.. code:: ipython3

    mesh.vertices()


.. parsed-literal::

    <dict_keyiterator at 0x60d74f278>


.. code:: ipython3

    mesh.faces()


.. parsed-literal::

    <generator object Mesh.faces at 0x60d723e08>


.. code:: ipython3

    mesh.edges()


.. parsed-literal::

    <generator object Mesh.edges at 0x60d723a98>


.. code:: ipython3

    for key in mesh.vertices():
        print(key)


.. parsed-literal::

    0
    1
    2
    3
    ...
    32
    33
    34
    35


.. code:: ipython3

    for key in mesh.faces():
        print(key)


.. parsed-literal::

    0
    1
    2
    3
    ...
    21
    22
    23
    24


.. code:: ipython3

    for key in mesh.edges():
        print(key)


.. parsed-literal::

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

.. code:: ipython3

    list(mesh.vertices())


.. parsed-literal::

    [0, 1, 2, 3, ... 32, 33, 34, 35]


.. code:: ipython3

    list(mesh.faces())


.. parsed-literal::

    [0, 1, 2, 3, ... 21, 22, 23, 24]


.. code:: ipython3

    list(mesh.edges())


.. parsed-literal::

    [(0, 1), (0, 6), (1, 7), (1, 2), ... (31, 32), (32, 33), (33, 34), (34, 35)]


Traversal
---------

.. code:: ipython3

    for key in mesh.vertices():
        print(key, "(neighbors)", mesh.vertex_neighbors(key, ordered=True))
        print(key, "(faces)", mesh.vertex_faces(key, ordered=True))
        print()


.. parsed-literal::

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
    

.. code:: ipython3

    for fkey in mesh.faces():
        print(fkey, "(vertices)", mesh.face_vertices(fkey))
        print(fkey, "(half-edges)", mesh.face_halfedges(fkey))
        print(fkey, "(neighbors)", mesh.face_neighbors(fkey))
        print()


.. parsed-literal::

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
    

Attributes
==========

All vertices, faces, and edges automatically have the default attributes
specified by the mesh class. The default vertex attributes are xyz
coordinates, with ``x=0``, ``y=0``, and ``z=0``. Edges and faces have no
default attributes.

To change the default attributes, do:

.. code:: ipython3

    mesh.update_default_vertex_attributes(z=10, is_fixed=False)

.. code:: ipython3

    mesh.update_default_face_attributes(is_loaded=True)

.. code:: ipython3

    mesh.update_default_edge_attributes(q=1.0)


Getting attributes
------------------

.. code:: ipython3

    mesh.get_vertex_attribute(mesh.get_any_vertex(), 'x')


.. parsed-literal::

    2.0


.. code:: ipython3

    mesh.get_vertices_attribute('x')


.. parsed-literal::

    [0.0, 2.0, 4.0, 6.0, ... 4.0, 6.0, 8.0, 10.0]


.. code:: ipython3

    mesh.get_vertices_attributes('xyz')


.. parsed-literal::

    [[0.0, 0.0, 0.0],
     [2.0, 0.0, 0.0],
     [4.0, 0.0, 0.0],
     [6.0, 0.0, 0.0],

     ...

     [4.0, 10.0, 0.0],
     [6.0, 10.0, 0.0],
     [8.0, 10.0, 0.0],
     [10.0, 10.0, 0.0]]


Setting attributes
------------------

.. code:: ipython3

    mesh.set_vertex_attribute(0, 'is_fixed', True)

.. code:: ipython3

    mesh.set_vertex_attributes(0, ('is_fixed', 'z'), (False, 10))

.. code:: ipython3

    mesh.set_vertices_attribute('z', 10)

.. code:: ipython3

    mesh.set_vertices_attributes(('z', 'is_fixed'), (0, False))


Serialisation
=============

Raw data
--------

.. code:: ipython3

    data = mesh.to_data()

.. code:: ipython3

    mesh = Mesh.from_data(data)


Json
----

.. code:: ipython3

    mesh.to_json('mesh.json')

.. code:: ipython3

    mesh = Mesh.from_json('mesh.json')


Pickle
------

.. code:: ipython3

    mesh.dump('mesh.pickle')

.. code:: ipython3

    mesh.load('mesh.pickle')

.. code:: ipython3

    s = mesh.dumps()

.. code:: ipython3

    mesh.loads(s)


Visualisation
=============

.. plot::
    :include-source:

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    
    plotter = MeshPlotter(mesh)
    
    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in mesh.vertices_on_boundary()},
        radius={key: 0.3 for key in mesh.vertices_on_boundary()},
        text={key: str(key) for key in mesh.vertices_on_boundary()}
    )
    plotter.draw_edges(
        color={key: '#00ff00' for key in mesh.edges_on_boundary()},
        width={key: 3 for key in mesh.edges_on_boundary()}
    )
    plotter.draw_faces(
        text={key: str(key) for key in mesh.faces_on_boundary()}
    )
    
    plotter.show()
