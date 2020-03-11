********************************************************************************
Networks
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

.. code-block:: python

    from compas.datastructures import Network

    network = Network()


Adding vertices and edges
=========================

.. code-block:: python

    >>> a = network.add_vertex()
    >>> b = network.add_vertex(x=1.0)
    >>> c = network.add_vertex(y=1.0)
    >>> d = network.add_vertex(x==1.0)
    >>> e = network.add_vertex(y==1.0)


.. code-block:: python

    >>> network.add_edge(a, b)
    (0, 1)
    >>> network.add_edge(a, c)
    (0, 2)
    >>> network.add_edge(a, d)
    (0, 3)
    >>> network.add_edge(a, e)
    (0, 4)


Identifiers
===========

All vertices in a network have a unique id, the *key* of the vertex. By
default, keys are integers, and every vertex is assigned a number
corresponding to the order in which they are added. The number is always
the highest number used so far, plus one.

Other types keys may be specified as well, as long as their value is
*hashable*.


.. code-block:: python

    >>> print(a, type(a))
    0 <class 'int'>

.. code-block:: python

    >>> b == a + 1
    True

.. code-block:: python

    >>> f = network.add_vertex(key=7)
    >>> f == e + 1
    False

.. code-block:: python

    >>> g = network.add_vertex()
    >>> g == f + 1
    True

.. code-block:: python

    >>> network.add_vertex(key='compas')
    'compas'

.. code-block:: python

    >>> network.add_vertex()
    9


Data
====

Iteration
---------

.. code-block:: python

    >>> network.vertices()
    <dict_keyiterator at 0x6193a2958>

.. code-block:: python

    >>> network.edges()
    <generator object Network.edges at 0x61560f678>

.. code-block:: python

    >>> for key in network.vertices():
    ...     print(key)
    ...
    0
    1
    2
    3
    4
    7
    8
    compas
    9

.. code-block:: python

    >>> for u, v in network.edges():
    ...     print(u, v)
    ...
    0 1
    0 2
    0 3
    0 4


Lists
-----

.. code-block:: python

    >>> list(network.vertices())
    [0, 1, 2, 3, 4, 7, 8, 'compas', 9]

.. code-block:: python

    >>> list(network.edges())
    [(0, 1), (0, 2), (0, 3), (0, 4)]


Filtering
---------

.. code-block:: python

    >>> network.vertices_where({'x': 0.0})
    <generator object VertexFilter.vertices_where at 0x61560f468>


Attributes
==========

All vertices and edges automatically have the default attributes. The
default vertex attributes are xyz coordinates, with ``x=0``, ``y=0`` and
``z=0``. Edges have no defaults.

To change the default attributes associated with vertices and edges, do:

.. code-block:: python

    >>> network.update_default_vertex_attributes({'z': 10}, is_fixed=False)
    >>> network.update_default_vertex_attributes(z=10, is_fixed=False)

.. code-block:: python

    >>> network.update_default_edge_attributes({'weight': 0.0})
    >>> network.update_default_edge_attributes(weight=0.0)

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

.. code-block:: python

    >>> network.get_vertex_attribute(a, 'is_fixed')
    False

.. code-block:: python

    >>> network.get_vertices_attribute('x')
    [0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0]

.. code-block:: python

    >>> network.get_vertices_attributes('xyz')
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0],
    [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0]]


Setting attributes
------------------

.. code-block:: python

    >>> network.set_vertex_attribute(a, 'is_fixed', True)
    >>> network.set_vertices_attribute('is_fixed', True)
    >>> network.set_vertices_attributes(('z', 'is_fixed'), (3, False))


Using constructors
==================

.. code-block:: python

    # network = Network.from_data(data)
    # network = Network.from_lines([([], []), ([], [])])
    # network = Network.from_json('network.json')
    # network = Network.from_pickle('network.pickle')

    >>> network = Network.from_obj(compas.get('lines.obj'))

.. note::

    COMPAS provides sample data for debugging purposes.
    This data can be accessed using :func:`compas.get`.


From/To
=======

.. code-block:: python

    >>> network = Network.from_obj(compas.get('lines.obj'))
    >>> data = network.to_data()
    >>> other = Network.from_data(data)


Queries
=======


Visualisation
=============

To create a 2D representation of a network, use a plotter.

.. code-block:: python

    from compas_plotters import NetworkPlotter

