.. _working-with-networks:

********
Networks
********

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
