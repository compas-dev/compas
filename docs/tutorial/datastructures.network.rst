********************************************************************************
Working with networks
********************************************************************************

COMPAS networks are simple edge graphs: they consist of vertices connected by edges.
Not all vertices have to be connected by edges.
A network without edges is a valid network.
In fact, even a network without vertices and edges is a valid network, albeit a quite pointless one.

Edges have a direction.
There can only be one edge between two vertices in a particular direction.
However, there can be two edges between two vertices in opposite direction.

Vertices can be connected to themseleves.


Making a network
================

.. code-block:: python

    import compas
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
