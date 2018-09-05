********************************************************************************
Networks
********************************************************************************

**COMPAS** networks are simple edge graphs: they consist of vertices connected by edges.
Not all vertices have to be connected by edges.
A network without edges is a valid network.
In fact, even a network without vertices is a valid network, albeit a quite pointless one.

Edges have a direction.
There can only be one edge between two vertices in a particular direction.
However, there can be two edges between two vertices in opposite direction.
Vertices can be connected to themseleves.


Making a network
================

.. code-block:: python

    from compas.datastructures import Network

    network = Network()


Adding vertices and edges
=========================

.. code-block:: python

    a = network.add_vertex()
    b = network.add_vertex(x=1.0)
    c = network.add_vertex(y=1.0)
    d = network.add_vertex(x=-1.0)
    e = network.add_vertex(y=-1.0)

.. code-block:: python

    network.add_edge(a, b)
    network.add_edge(a, c)
    network.add_edge(a, d)
    network.add_edge(a, e)


Identifiers
===========

All vertices in a network have a unique id, the *key* of the vertex.
By default, keys are integers, and every vertex is assigned a number corresponding to the order in which they are added.
The number is always the highest number used so far, plus one.

Other types keys may be specified as well, as long as their value is *hashable*.

.. code-block:: python

    print(a, type(a))

    # 0 <class 'int'>

.. code-block:: python

    b == a + 1

    # True

.. code-block:: python

    f = network.add_vertex(key=7)
    f == e + 1

    # False

.. code-block:: python

    g = network.add_vertex()
    g == f + 1

    # True

.. code-block:: python

    network.add_vertex(key='compas')

    # 'compas'

.. code-block:: python

    network.add_vertex()

    # 9


Data
====

.. code-block:: python

    network.vertices()

    # <dict_keyiterator object at 0x1104280e8>

.. code-block:: python

    network.edges()

    # <generator object Network.edges at 0x112fc1990>

.. code-block:: python

    for key in network.vertices():
        # do stuff

.. code-block:: python

    for u, v in network.edges():
        # do stuff

.. code-block:: python

    vertices = list(network.vertices())

.. code-block:: python

    edges = list(network.edges())


Attributes
==========

All vertices and edges automatically have the default attributes.
The default vertex attributes are xyz coordinates, with ``x=0``, ``y=0`` and ``z=0``.
Edges have no defaults.

To change the default attributes associated with vertices and edges, do:

.. code-block:: python

    network.update_default_vertex_attributes({'z' : 10, 'is_fixed' : False})

    # or network.update_default_vertex_attributes({z=10, is_fixed=False)

.. code-block:: python

    network.update_default_edge_attributes({'weight': 0.0})

    # or network.update_default_edge_attributes(weight=0.0)

.. note::

    Other attributes then the ones specified in the defaults can also be added.
    However, these attributes then only exist on the vertices or edges where they have been specified.
    To prevent this and only allow the registered attributes to be added, set ``Network.strict_attributes = True``.

    When a vertex or edge is added to the network, the default attributes are copied and the values of the specified attributes are modified.
    To only store the modified values, set ``Network.copy_defaults = False``.


Getting attributes
------------------

.. code-block:: python

    network.get_vertex_attribute(a, 'is_fixed')

    # False

.. code-block:: python

    network.get_vertices_attribute('x')

    # [0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
