********************************************************************************
Working with networks
********************************************************************************

COMPAS networks are simple edge graphs: they consist of vertices
connected by edges. Not all vertices have to be connected by edges. A
network without edges is a valid network. In fact, even a network
without vertices and edges is a valid network, albeit a quite pointless
one.

Edges have a direction. There can only be one edge between two vertices
in a particular direction. However, there can be two edges between two
vertices in opposite direction. Vertices can be connected to
themseleves.

Check out the docs for detailed information about the network and the available
functionality: :class:`compas.datastructures.Network`.


Making a network
================

.. code:: ipython3

    import compas
    from compas.datastructures import Network

    network = Network()


Adding vertices and edges
=========================

.. code:: ipython3

    a = network.add_vertex()
    b = network.add_vertex(x=1.0)
    c = network.add_vertex(y=1.0)
    d = network.add_vertex(x==1.0)
    e = network.add_vertex(y==1.0)


.. code:: ipython3

    network.add_edge(a, b)
    network.add_edge(a, c)
    network.add_edge(a, d)
    network.add_edge(a, e)


.. parsed-literal::

    (0, 4)


Identifiers
===========

All vertices in a network have a unique id, the *key* of the vertex. By
default, keys are integers, and every vertex is assigned a number
corresponding to the order in which they are added. The number is always
the highest number used so far, plus one.

Other types keys may be specified as well, as long as their value is
*hashable*.


.. code:: ipython3

    print(a, type(a))


.. parsed-literal::

    0 <class 'int'>


.. code:: ipython3

    b == a + 1


.. parsed-literal::

    True


.. code:: ipython3

    f = network.add_vertex(key=7)
    f == e + 1


.. parsed-literal::

    False


.. code:: ipython3

    g = network.add_vertex()
    g == f + 1


.. parsed-literal::

    True


.. code:: ipython3

    network.add_vertex(key='compas')


.. parsed-literal::

    'compas'


.. code:: ipython3

    network.add_vertex()


.. parsed-literal::

    9


Data
====

Iteration
---------

.. code:: ipython3

    network.vertices()


.. parsed-literal::

    <dict_keyiterator at 0x6193a2958>


.. code:: ipython3

    network.edges()


.. parsed-literal::

    <generator object Network.edges at 0x61560f678>


.. code:: ipython3

    for key in network.vertices():
        print(key)


.. parsed-literal::

    0
    1
    2
    3
    4
    7
    8
    compas
    9


.. code:: ipython3

    for u, v in network.edges():
        print(u, v)


.. parsed-literal::

    0 1
    0 2
    0 3
    0 4


Lists
-----

.. code:: ipython3

    list(network.vertices())


.. parsed-literal::

    [0, 1, 2, 3, 4, 7, 8, 'compas', 9]


.. code:: ipython3

    list(network.edges())


.. parsed-literal::

    [(0, 1), (0, 2), (0, 3), (0, 4)]


Filtering
---------

.. code:: ipython3

    network.vertices_where({'x': 0.0})


.. parsed-literal::

    <generator object VertexFilter.vertices_where at 0x61560f468>


Attributes
==========

All vertices and edges automatically have the default attributes. The
default vertex attributes are xyz coordinates, with ``x=0``, ``y=0`` and
``z=0``. Edges have no defaults.

To change the default attributes associated with vertices and edges, do:

.. code:: ipython3

    network.update_default_vertex_attributes({'z': 10}, is_fixed=False)

    # or network.update_default_vertex_attributes(z=10, is_fixed=False)

.. code:: ipython3

    network.update_default_edge_attributes({'weight': 0.0})

    # or network.update_default_edge_attributes(weight=0.0)

.. note::

    Other attributes then the ones specified in the defaults can also be
    added. However, these attributes then only exist on the vertices or
    edges where they have been specified. To prevent this and only allow the
    registered attributes to be added, set
    ``Network.strict_attributes = True``.

    When a vertex or edge is added to the network, the default attributes
    are copied and the values of the specified attributes are modified. To
    only store the modified values, set ``Network.copy_defaults = False``.


Getting attributes
------------------

.. code:: ipython3

    network.get_vertex_attribute(a, 'is_fixed')


.. parsed-literal::

    False


.. code:: ipython3

    network.get_vertices_attribute('x')


.. parsed-literal::

    [0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0]


.. code:: ipython3

    network.get_vertices_attributes('xyz')


.. parsed-literal::

    [[0.0, 0.0, 0.0],
     [1.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [-1.0, 0.0, 0.0],
     [0.0, -1.0, 0.0],
     [0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0]]


Setting attributes
------------------

.. code:: ipython3

    network.set_vertex_attribute(a, 'is_fixed', True)

.. code:: ipython3

    network.set_vertices_attribute('is_fixed', True)

.. code:: ipython3

    network.set_vertices_attributes(('z', 'is_fixed'), (3, False))


Using constructors
==================

.. code:: ipython3

    # network = Network.from_data(data)
    # network = Network.from_lines([([], []), ([], [])])
    # network = Network.from_json('network.json')
    # network = Network.from_pickle('network.pickle')

    network = Network.from_obj(compas.get('lines.obj'))


Queries
=======

under construction...


Visualisation
=============

To create a 2D representation of a network, use a plotter.

.. code:: ipython3

    from compas.plotters import NetworkPlotter

