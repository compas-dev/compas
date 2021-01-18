********
Networks
********

.. rst-class:: lead

Networks are very flexible data structures.
They can, for example, be used to represent the elements of a cablenet,
or even to keep track of the relationships between the individual elements
of a Discrete Element Assembly.


Data structure
==============

In COMPAS a network is a "directed edge graph"
that encodes the relationships between "nodes" with "edges".
Not all nodes have to be connected by edges.
In fact, even a network without edges is a valid network.

Edges have a direction.
There can only be one edge between two nodes in a particular direction.
However, there can be two edges between the same two nodes
in opposite direction.


Building a Network
==================

Networks can be built from scratch by adding nodes and edges.

::

    >>> from compas.datastructures import Network

    >>> network = Network()

    >>> a = network.add_node()  # x, y, z coordinates are optional and default to x=0, y-0, z=0
    >>> b = network.add_node(x=1)
    >>> c = network.add_node(y=1)
    >>> d = network.add_node(x=-1)
    >>> e = network.add_node(y=-1)

    >>> network.add_edge(a, b)
    >>> network.add_edge(a, c)
    >>> network.add_edge(a, d)
    >>> network.add_edge(a, e)


Constructors
============

Building a network node per node and edge per edge is fine for very simple Networks
but quickly becomes tedious for networks of relevant size.
