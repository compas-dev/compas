.. _tutorial_datastructures:

********************************************************************************
Working with datastructures
********************************************************************************

.. sectionauthor:: Tom Van Mele 

.. add code-generated image or images here


Network, Mesh and VolMesh
=========================

:mod:`compas.datastructures` defines three datastructures:
``Network``, ``Mesh``, and ``VolMesh``, and algorithms and operations for each
of them. Each of the datastructures and their corresponding functionality are
defined in their own subpackage.


* compas.datastructures

  * mesh

    * mesh
    * operations
    * algorithms

  * network

    * network
    * operations
    * algorithms

  * volmesh

    * volmesh
    * operations
    * algorithms


The datastructure classes can be imported directly from the datastructures package.

.. code-block:: python

    >>> from compas.datastructures import Network
    >>> from compas.datastructures import Mesh
    >>> from compas.datastructures import VolMesh

The operations and algorithms have been namespaced and pulled up so they can be
imported directly from the datastructures package as well.

.. code-block:: python
    
    >>> from compas.datastructures import network_dijkstra_path
    >>> from compas.datastructures import mesh_collapse_edge

The ``Network`` is implemented as a directed graph. Each edge connects two and only
two vertices, pointing from one of the vertices to the other. Between two vertices
no more than two edges can exist and they must point in opposite directions. The
``Network`` has no faces.

The ``Mesh`` is implemented as a halfedge datastructure. It can be used to represent
polygonal surface meshes. Faces can be triangles, quads, and N-sided polygons.
All faces are assumed closed, which means that the first and last vertex of a face
definition are not the same. ...

The ...


Builders and constructors
=========================

Every datastructure has a default constructor, builder methods, and
a series of specialised constructor functions that build datastructures in a
specific way. The default constructor creates an empty datastructure instance.

.. code-block:: python

    >>> network = Network()
    >>> mesh = Mesh()
    >>> volmesh = VolMesh()


With the builders data can be added to the empyty containers. Each of the
datastructures has its own builder methods. 
The ``Network`` defines ``Network.add_vertex`` and ``Network.add_edge``,
the ``Mesh`` defines ``Mesh.add_vertex`` and ``Mesh.add_face``,
and the ``VolMesh`` defines ``VolMesh.add_vertex`` and ``VolMesh.add_cell``.

.. code-block:: python
    
    >>> a = network.add_vertex()
    >>> b = network.add_vertex()
    >>> network.add_edge(a, b)
    (0, 1)

The builders always return the identifiers (*keys*) of the element(s) they created.
In the above example, the vertex builder returned ``0`` and ``1``, which were assigned
to the variables ``a`` and ``b``. The edge builder returned the tuple ``(0, 1)``,
indicating it had added an edge from vertex ``0`` to vertex ``1``.

It is also possible to specify the *keys* of the vertices. Any hashable type can
be used as a key. This roughly means ``int``, ``float``, ``str``, ``tuple``, and
``frozenset``, or any object that implements the magic method ``__hash__``. If no
key is provided, the datastructure will automatically assign an integer. It keeps
track of the highest integer that was used so far, and increments that value by one.

.. code-block:: python
    
    >>> network.add_vertex()
    0
    >>> network.add_vertex(3)
    3
    >>> network.add_vertex()
    4
    >>> network.add_vertex('1')
    '1'
    >>> network.add_vertex((5, 3))
    (5, 3)
    >>> network.add_vertex(3.14159)
    3.14159
    >>> network.add_vertex()
    5

The builders also provide the possibility to add data attributes in the form of
attribute dictionaries or keyword arguments (*kwargs*).
Note that all datastructures (can) define default data attributes for the different
types of data. For examples, all three datastructures automatically assign XYZ
coordinates to all vertices, with a default value of ``x = 0.0, y = 0.0, z = 0.0``.
This means that all following statements are equivalent and add a vertex with
coordinates (``1.0, 0.0, 0.0``).

.. code-block:: python
    
    >>> network.add_vertex(x=1.0)
    >>> network.add_vertex(x=1.0, y=0.0)
    >>> network.add_vertex(x=1.0, z=0.0)
    >>> network.add_vertex(x=1.0, y=0.0, z=0.0)
    >>> network.add_vertex(attr_dict={'x': 1.0})
    >>> network.add_vertex(attr_dict={'x': 5.0}, x=1.0)
    >>> network.add_vertex(attr_dict={'y': 3.0}, x=1.0, y=0.0)

The allowable attributes are not limited to the default attributes.

.. code-block:: python
    
    >>> network.add_vertex(attr_dict={'x': 1.0, 'y': 1.0, 'z': 1.0, 'is_fixed': True})
    >>> network.add_vertex(x=1.0, y=1.0, z=1.0, is_fixed=True)

The mechanism is the same for edges.

.. code-block:: python

    >>> network.add_edge(0, 1, attr_dict={'q': 1.0, 'fmin': 0.0, 'fmax': 10.0})
    >>> network.add_edge(0, 1, q=1.0, fmin=0.0, fmax=10.0)

All of the above also applies to the ``Mesh`` and ``VolMesh`` datastructures.

.. code-block:: python

    >>> mesh.add_vertex() 
    >>> mesh.add_vertex()
    >>> mesh.add_vertex()

For convencience, all datastructures come with specialised alternative constructors.
These are implemented as class methods (using the ``@classmethod`` decoreator) and
are named using the following pattern ``.from_xxx``.

.. code-block:: python

    >>> network = Network.from_data(...)
    >>> network = Network.from_json(...)
    >>> network = Network.from_obj(...)
    >>> network = Network.from_vertices_and_edges(...)
    >>> network = Network.from_lines(...)

.. code-block:: python

    >>> mesh = Mesh.from_data(...)
    >>> mesh = Mesh.from_json(...)
    >>> mesh = Mesh.from_obj(...)
    >>> mesh = Mesh.from_vertices_and_faces(...)
    >>> mesh = Mesh.from_polygons(...)
    >>> mesh = Mesh.from_polyhedron(...)
    >>> mesh = Mesh.from_points(...)

.. code-block:: python

    >>> volmesh = VolMesh.from_data(...)
    >>> volmesh = VolMesh.from_json(...)
    >>> volmesh = VolMesh.from_obj(...)
    >>> volmesh = VolMesh.from_vertices_and_cells(...)
    >>> volmesh = VolMesh.from_polyhedrons(...)

``compas`` also provides sample data that can be used together with the constructors.

.. code-block:: python
    
    >>> import compas
    >>> from compas.datastructures import Network
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    

General info
============

Use the ``print`` function (or ``print`` statement in Python 2.x) to display
general information about the datastructure instance.

.. code-block:: python

    >>> network = Network()
    >>> print(network)

.. code-block:: none

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    network: Network
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    - default vertex attributes

    y => 0.0
    x => 0.0
    z => 0.0

    - default edge attributes

    None

    - number of vertices: 0
    - number of edges: 0

    - vertex degree min: 0
    - vertex degree max: 0

.. code-block:: python

    >>> mesh = Mesh()
    >>> print(mesh)

.. code-block:: none

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    mesh: Mesh
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    - default vertex attributes

    y => 0.0
    x => 0.0
    z => 0.0

    - default edge attributes

    None

    - default face attributes

    None

    - number of vertices: 0
    - number of edges: 0
    - number of faces: 0

    - vertex degree min: 0
    - vertex degree max: 0

    - face degree min: None
    - face degree max: None

.. code-block:: python

    >>> volmesh = VolMesh()
    >>> print(volmesh)

.. code-block:: none

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    volmesh: VolMesh
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Accessing the data
==================

Every datastructure exposes several functions to access its data.
All of those *accessors* are iterators; they are meant to be iterated over.
Lists of data have to be constructed explicitly.

.. code-block:: python

    >>> import compas
    >>> from compas.datastructures import Network
    >>> network = Network.from_obj(compas.get_data('lines.obj'))

.. code-block:: python

    >>> network.vertices()
    <dictionary-keyiterator object at 0x10f030e68>

.. code-block:: python
    
    >>> len(network.vertices())
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: object of type 'dictionary-keyiterator' has no len()

.. code-block:: python

    >>> list(network.vertices())
    [0, 1, 2, ..., 29, 30, 31]
    >>> len(list(network.vertices()))
    32
    >>> network.number_of_vertices()
    32

.. code-block:: python
    
    >>> for key in mesh.vertices():
    ...     print(key)
 
    0
    1
    2
    ...
    29
    30
    31

The same applies to the edges.
The accessor is an iterator; it is meant for iterating over the edges.
To count the edges or to get a list of edges, the iterator needs to be converted
explicitly.

.. code-block:: python
    
    >>> network.edges()
    <generator object edges at 0x10f03d140>

.. code-block:: python
    
    >>> len(network.edges())
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: object of type 'generator' has no len()

.. code-block:: python

    >>> list(network.edges())
    [(0, 3), (0, 19), (2, 30), ..., (30, 17), (31, 16), (31, 25)]
    >>> len(list(network.edges())
    40
    >>> network.number_of_edges()
    40

.. code-block:: python
    
    >>> for u, v in network.edges():
    ...     print(u, v)

    0 3
    0 19
    2 30
    ...
    30 17
    31 16
    31 25


Accessing the data attributes
=============================

The data attributes can be accessed in several ways.
First as a modifier of the iterators.

.. code-block:: python

    >>> for key, attr in network.vertices(data=True):
    ...     print(key, attr)

    0 {'y': 8.0, 'x': 2.0, 'z': 0.0}
    1 {'y': 10.0, 'x': 8.0, 'z': 0.0}
    2 {'y': 6.0, 'x': 0.0, 'z': 0.0}
    ...
    29 {'y': 4.0, 'x': 4.0, 'z': 0.0}
    30 {'y': 6.0, 'x': 2.0, 'z': 0.0}
    31 {'y': 2.0, 'x': 8.0, 'z': 0.0}

Second through dedicated attribute accessors.

.. code-block:: python

    >>> network.get_vertex_attribute(0, 'x')
    2.0
    >>> network.get_vertex_attributes(0, 'xyz')
    [2.0, 8.0, 0.0]
    >>> network.get_vertices_attribute('x')
    [2.0, 8.0, 0.0, ..., 4.0, 2.0, 8.0]
    >>> network.get_vertices_attributes('xyz')
    [[2.0, 8.0, 0.0], [8.0, 10.0, 0.0], [0.0, 6.0, 0.0], ..., [4.0, 4.0, 0.0], [2.0, 6.0, 0.0], [8.0, 2.0, 0.0]]


Accessing topological data
==========================

The available functions for accessing the topological data depend on the type of
datastructure, although they obviously have a few of them in common.
In case of the ``Network``, all topological functions have to do with the adjacency
relationship of the vertices.

.. code-block:: python
    
    # undirected
    
    >>> network.vertex_neighbours()
    >>> network.vertex_degree()
    >>> network.vertex_
    >>> network.edge_

.. code-block:: python

    >>> mesh.vertex_neighbours()
    >>> mesh.vertex_degree()
    >>> mesh.vertex_faces()
    >>> mesh.vertex_neighbourhood()
    >>> mesh.vertex_
    >>> mesh.faces_vertices()
    >>> mesh.face_neighbours()
    >>> mesh.face_neighbourhood()
    >>> mesh.face_
    >>> mesh.edge_faces()


Accessing geometric data
========================

.. note to self
   
    - every function that ends up being used in a list comprehension
      should have a single-call equivalent, with an optional key parameter

.. code-block:: python

    >>> network.vertex_coordinates()
    >>> network.vertex_
    >>> network.edge_coordinates()
    >>> network.edge_vector()
    >>> network.edge_direction()
    >>> network.edge_length()
    >>> network.edge_midpoint()
    >>> network.edge_

.. code-block:: python

    >>> mesh.vertex_coordinates()
    >>> mesh.vertex_area()
    >>> mesh.vertex_centroid()
    >>> mesh.vertex_
    >>> mesh.face_area()
    >>> mesh.face_centroid()
    >>> mesh.face_center()
    >>> mesh.face_frame()
    >>> mesh.face_circle()
    >>> mesh.face_normal()
    >>> mesh.face_
    >>> mesh.edge_coordinates()
    >>> mesh.edge_vector()
    >>> mesh.edge_direction()
    >>> mesh.edge_length()
    >>> mesh.edge_midpoint()
    >>> mesh.edge_


Modifying the data
==================

.. ?
    
    - add_vertex
    - add_edge
    - add_face
    - delete/remove => remove!
    - operations?


Modifying the data attributes
=============================

.. code-block:: python

    >>> network.set_vertex_attribute()
    >>> network.set_vertex_attributes()
    >>> network.set_vertices_attribute()
    >>> network.set_vertices_attributes()

.. code-block:: python

    >>> network.set_edge_attribute()
    >>> network.set_edge_attributes()
    >>> network.set_edges_attribute()
    >>> network.set_edges_attributes()


Serialisation
=============

.. code-block:: python

    >>> data = network.to_data()
    >>> data = network.data

.. code-block:: python

    >>> network = Network.from_data()
    >>> network.data = data

.. code-block:: python
    
    >>> import json
    >>> with open('data.json', 'w') as f:
    ...     json.dump(f, network.to_data())
    ...

.. code-block:: python
    
    >>> import json
    >>> network = Network()
    >>> with open('data.json', 'r') as f:
    ...     network.data = json.load(f)

.. code-block:: python
    
    >>> network.to_json('data.json')

.. code-block:: python
    
    >>> network = Network.from_json('data.json')


Visualisation
=============

.. note::

    This section describes the visualisation options with the core viewers and plotters.
    For visualisation in CAD software see:
    
    * compas_rhino.artists
    * compas_blender.xxx
    * ...


.. code-block:: python

    >>> import compas
    >>> from compas.visualization.plotters import NetworkPlotter
    >>> from compas.datastructures import Network
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    >>> plotter = NetworkPlotter(network)
    >>> plotter.draw_vertices()
    >>> plotter.draw_edges()
    >>> plotter.show()

.. raw:: html

    <figure class="figure figure-plot">

.. plot::

    import compas
    from compas.visualization.plotters import NetworkPlotter
    from compas.datastructures import Network
    network = Network.from_obj(compas.get_data('lines.obj'))
    plotter = NetworkPlotter(network)
    plotter.draw_vertices()
    plotter.draw_edges()
    plotter.show()

.. raw:: html

    <figcaption class="figure-caption"></figcaption>
    </figure>


.. code-block:: python

    >>> plotter.draw_vertices(text={...}, facecolor={...}, edgecolor={...}, radius={...})

.. code-block:: python

    >>> plotter.draw_edges(text={...}, color={...}, width={...})


Operations & Algorithms
=======================


Customisation
=============

.. code-block:: python
    
    >>> network = Network.from_obj(compas.get_data('lines.obj'))
    >>> network.update_default_vertex_attributes({...})
    >>> network.update_default_edge_attributes({...})
    >>> network.get_vertex_attributes(network.get_any_vertex())
    >>> print(network)

.. code-block:: python
    
    >>> class SpecialNetwork(Network):
    ...     def __init__(self):
    ...         super(SpecialNetwork, self).__init__()
    ...         self.default_vertex_attributes.update({...})
    ...         self.default_edge_attributes.update({...})
    ...


Numerical computation
=====================

.. code-block:: python

    >>> class NumericalNetwork(NumericalMixin, Network):
    ...     pass
    ...
    >>> network = NumericalNetwork.from_obj('lines.obj')

.. code-block:: python

    >>> network = Network.from_obj('lines.obj', mixins=(NumericalMixin, ))

.. code-block:: python

    >>> network = Network.from_obj('lines.obj')
    >>> network.mix_in((NumericalMixin, ))

.. code-block:: python
    
    >>> C = network.connectivity_matrix()
    >>> xyz = network.vertices_array()
    >>> C.dot(xyz)


Example
=======



