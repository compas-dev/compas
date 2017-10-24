.. _acadia2017_day1_datastructures:

********************************************************************************
Datastructures
********************************************************************************


Why data structures?
====================

Consider set of points and faces.
How would you answer basic questions about the connectivity of these objects?
For example:

* Which vertices are connected to a particular vertex?
* Which faces are connected to a particular vertex?
* Which vertices make up a particular face?
* Which faces are connected to a particular face?
* ...

.. code-block:: python

    # geometrical solution to some of these questions


By structuring the data, these questions can be answered topologically rather than
geometrically, which is much more efficient.

Applications ...


Network, Mesh, VolMesh
----------------------

The *compas* framework contains three types of data structures and related operations and algorithms:

* ``compas.datastructures.network``
* ``compas.datastructures.mesh``
* ``compas.datastructures.volmesh``


Builders and constructors
=========================

Every datastructure has a default constructor, builder methods, and
a series of specialised constructor functions that build datastructures in a
specific way. The default constructor creates an empty datastructure instance.

.. code-block:: python

    mesh = Mesh()


With the builders data can be added to the empyty containers. Each of the
datastructures has its own builder methods.
The ``Mesh`` defines ``Mesh.add_vertex`` and ``Mesh.add_face``.

.. code-block:: python
    
    a = mesh.add_vertex()
    b = mesh.add_vertex()
    c = mesh.add_vertex()
    abc = mesh.add_face([a, b, c])

    print(a, b, c)
    print(abc)

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
    
    print(mesh.add_vertex())
    print(mesh.add_vertex(3))
    print(mesh.add_vertex())
    print(mesh.add_vertex('1'))
    print(mesh.add_vertex((5, 3)))
    print(mesh.add_vertex(3.14159))
    print(mesh.add_vertex())

The builders also provide the possibility to add data attributes in the form of
attribute dictionaries or keyword arguments (*kwargs*).
Note that all datastructures (can) define default data attributes for the different
types of data. For examples, all three datastructures automatically assign XYZ
coordinates to all vertices, with a default value of ``x = 0.0, y = 0.0, z = 0.0``.
This means that all following statements are equivalent and add a vertex with
coordinates (``1.0, 0.0, 0.0``).

.. code-block:: python
    
    mesh.add_vertex(x=1.0)
    mesh.add_vertex(x=1.0, y=0.0)
    mesh.add_vertex(x=1.0, z=0.0)
    mesh.add_vertex(x=1.0, y=0.0, z=0.0)
    mesh.add_vertex(attr_dict={'x': 1.0})
    mesh.add_vertex(attr_dict={'x': 5.0}, x=1.0)
    mesh.add_vertex(attr_dict={'y': 3.0}, x=1.0, y=0.0)

The allowable attributes are not limited to the default attributes.

.. code-block:: python
    
    mesh.add_vertex(attr_dict={'x': 1.0, 'y': 1.0, 'z': 1.0, 'is_fixed': True})
    mesh.add_vertex(x=1.0, y=1.0, z=1.0, is_fixed=True)

The mechanism is the same for faces.

.. code-block:: python

    mesh.add_face([0, 1, 2], attr_dict={'t': 1.0, 'density': 2.5})
    mesh.add_face([0, 1, 2], t=1.0, density=2.5)

For convencience, all datastructures come with specialised alternative constructors.
These are implemented as class methods (using the ``@classmethod`` decoreator) and
are named using the following pattern ``.from_xxx``.

.. code-block:: python

    mesh = Mesh.from_data(...)
    mesh = Mesh.from_json(...)
    mesh = Mesh.from_obj(...)
    mesh = Mesh.from_vertices_and_faces(...)
    mesh = Mesh.from_polygons(...)
    mesh = Mesh.from_polyhedron(...)
    mesh = Mesh.from_points(...)

``compas`` also provides sample data that can be used together with the constructors.

.. code-block:: python
    
    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))


General info
============

Use the ``print`` function to display general information about the datastructure instance.

.. code-block:: python

    mesh = Mesh()
    print(mesh)


Accessing the data
==================

Every datastructure exposes several functions to access its data.
All of those *accessors* are iterators; they are meant to be iterated over.
Lists of data have to be constructed explicitly.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    mesh = Mesh.from_obj(compas.get('faces.obj'))

    print(mesh.vertices())
    # <dictionary-keyiterator object at 0x10f030e68>

    print(len(mesh.vertices()))
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # TypeError: object of type 'dictionary-keyiterator' has no len()

    print(list(mesh.vertices()))
    # [0, 1, 2, ..., 29, 30, 31]

    print(len(list(mesh.vertices())))
    # 32

    print(mesh.number_of_vertices())
    # 32

    for key in mesh.vertices():
        print(key)

The same applies to the faces.
The accessor is an iterator; it is meant for iterating over the faces.
To count the faces or to get a list of faces, the iterator needs to be converted
explicitly.

.. code-block:: python
    
    print(mesh.faces())
    # <generator object edges at 0x10f03d140>

    print(len(mesh.faces()))
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # TypeError: object of type 'generator' has no len()

    print(list(mesh.faces()))
    # [(0, 3), (0, 19), (2, 30), ..., (30, 17), (31, 16), (31, 25)]
    
    print(len(list(mesh.faces()))
    # 40

    print(mesh.number_of_faces())
    # 40

    for fkey in mesh.faces():
        print(fkey)


Accessing the data attributes
=============================

The data attributes can be accessed in several ways.
First using a modified call to the general accessor methods.

.. code-block:: python

    for key, attr in mesh.vertices(data=True):
        print(key, attr)

Second through dedicated attribute accessors.

.. code-block:: python

    mesh.get_vertex_attribute(0, 'x')
    mesh.get_vertex_attributes(0, 'xyz')
    mesh.get_vertices_attribute('x')
    mesh.get_vertices_attributes('xyz')


Modifying the data
==================

Modifying the data attribbutes
==============================

Visualization
=============

.. plot::
    :include-source:

    from __future__ import print_function
    
    import compas

    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices()
    plotter.draw_faces()
    plotter.draw_edges()
    plotter.show()


Topology
========

The available functions for accessing the topological data depend on the type of
datastructure, although they obviously have a few of them in common.

.. code-block:: python

    mesh.vertex_neighbours()
    mesh.vertex_degree()
    mesh.vertex_faces()
    mesh.vertex_neighbourhood()
    ...
    mesh.faces_vertices()
    mesh.face_neighbours()
    mesh.face_neighbourhood()
    ...

.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    key  = 17
    nbrs = mesh.vertex_neighbours(key, ordered=True)

    text   = {nbr: str(index) for index, nbr in enumerate(nbrs)}
    fcolor = {key: '#cccccc' for key in nbrs}

    fcolor[17] = '#ff0000'

    plotter.draw_vertices(text=text, facecolor=fcolor)
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()

.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices(text={key: mesh.vertex_degree(key) for key in mesh.vertices()})
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()


Geometry
========

.. code-block:: python

    mesh.vertex_coordinates()
    mesh.vertex_area()
    mesh.vertex_centroid()
    ...
    mesh.face_area()
    mesh.face_centroid()
    mesh.face_center()
    mesh.face_frame()
    mesh.face_circle()
    mesh.face_normal()
    ...
    mesh.edge_coordinates()
    mesh.edge_vector()
    mesh.edge_direction()
    mesh.edge_length()
    mesh.edge_midpoint()
    ...


.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices()
    plotter.draw_faces(text={fkey: '%.1f' % mesh.face_area(fkey) for fkey in mesh.faces()})
    plotter.draw_edges()

    plotter.show()

.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices(text={key: '%.1f' % mesh.vertex_area(key) for key in mesh.vertices()})
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()


Operations
==========

.. code-block:: python
    
    mesh.delete_vertex
    mesh.insert_vertex
    mesh.delete_face

    compas.datastructures.mesh_collapse_edge
    compas.datastructures.mesh_swap_edge
    compas.datastructures.mesh_split_edge

    compas.datastructures.trimesh_collapse_edge
    compas.datastructures.trimesh_swap_edge
    compas.datastructures.trimesh_split_edge


Algorithms
==========

.. code-block:: python
    
    compas.datastructures.mesh_subdivide
    compas.datastructures.mesh_dual
    compas.datastructures.mesh_delaunay_from_points
    compas.datastructures.mesh_voronoi_from_points

    compas.datastructures.trimesh_remesh

.. code-block:: python
    
    compas.geometry.smooth_centroid
    compas.geometry.smooth_centerofmass
    compas.geometry.smooth_area

.. code-block:: python
    
    compas.geometry.shortest_path
    compas.geometry.dijkstra_path


Customization
=============


Numerical computation
=====================


CAD integration
===============
