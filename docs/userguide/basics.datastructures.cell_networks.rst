********************************************************************************
Cell Networks
********************************************************************************

.. rst-class:: lead

A `compas.datastructures.CellNetwork` is a geometric implementation of a data structure for storing a
collection of mixed topologic entities such as cells, faces, edges and vertices.
It can be used to describe buildings; walls and floors can be represented as faces, columns, beams as edges, and rooms as cells.
Aperatures such as windows or doors could be stored as face attributes.
Topological queries such as "what is the building envelope" can be easily be derived.

.. note::

    Please refer to the API for a complete overview of all functionality:

    * :class:`compas.datastructures.HalfFace`
    * :class:`compas.datastructures.CellNetwork`


CellNetwork Construction
========================

Cell networks can be constructed in a number of ways:

* from scratch, by adding vertices, faces and cells one by one,
* using a special constructor function, or
* from the data contained in a file.


