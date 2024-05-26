********************************************************************************
Cell Networks
********************************************************************************

.. rst-class:: lead

A :class:`compas.datastructures.CellNetwork` uses a halfface data structure to represent a collection of mixed topologic entities (cells, faces, edges and vertices)
and to facilitate the application of topological and geometrical operations on it.
In addition, it provides a number of methods for storing arbitrary data on vertices, edges, faces, cells, and the overall cell network itself.

.. note::

    Please refer to the API for a complete overview of all functionality:

    * :class:`compas.datastructures.CellNetwork`
    * :class:`compas.datastructures.HalfFace`


CellNetwork Construction
========================

CellNetworks can be constructed in a number of ways:

* from scratch, by adding vertices, faces and cells one by one,
* using a special constructor function, or
* from the data contained in a file.

From Scratch
------------

>>> from compas.datastructures import CellNetwork
>>> cell_network = CellNetwork()
>>> vertices = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
>>> faces = [[0, 1, 2, 3], [0, 3, 5, 4],[3, 2, 6, 5], [2, 1, 7, 6],[1, 0, 4, 7],[4, 5, 6, 7]]
>>> cells = [[0, 1, 2, 3, 4, 5]]
>>> [cell_network.add_vertex(x=x, y=y, z=z) for x, y, z in vertices]
>>> [cell_network.add_face(fverts) for fverts in faces]
>>> [cell_network.add_cell(fkeys) for fkeys in cells]
>>> print(cell_network)
<CellNetwork with 8 vertices, 6 faces, 1 cells, 12 edges>

Using Constructors
------------------

>>> from compas.datastructures import CellNetwork
>>> cell_network = CellNetwork.from_vertices_and_cells(...)


From Data in a File
-------------------

>>> from compas.datastructures import CellNetwork
>>> cell_network = CellNetwork.from_obj(...)
>>> cell_network = CellNetwork.from_json(...)


Visualisation
=============

Like all other COMPAS geometry objects and data structures, cell networks can be visualised by placing them in a scene.
For more information about visualisation with :class:`compas.scene.Scene`, see :doc:`/userguide/basics.visualisation`.

>>> import compas
>>> from compas.datastructures import CellNetwork
>>> from compas.scene import Scene
>>> cell_network = CellNetwork.from_json(compas.get('cellnetwork_example.json'))
>>> scene = Scene()
>>> scene.add(mesh)
>>> scene.show()

.. figure:: /_images/userguide/basics.datastructures.cellnetworks.example_grey.png


Vertices, Edges, Faces, Cells
=============================

The cell network contains mixed topologic entities such as cells, faces, edges and vertices.
    * Vertices are identified by a positive integer that is unique among the vertices of the current mesh.
    * Edges are identified by a pair (tuple) of two vertex identifiers.
    * Faces are identified by a positive integer that is unique among the faces of the current mesh.
    * Cells are identified by a positive integer that is unique among the cells of the current mesh.

>>> cell_network = CellNetwork.from_json(compas.get('cellnetwork_example.json'))
>>> cell_network.number_of_vertices()
44
>>> cell_network.number_of_edges()
91
>>> cell_network.number_of_faces()
43
>>> cell_network.number_of_cells()
6

An edge can be assigned to any number of faces, or to none.

>>> cell_network.edge_faces((2, 6))
[2, 3, 39]
>>> cell_network.edge_faces((1, 10))
[8]
>>> cell_network.edges_without_face()
[(43, 34)]

A face can be at maximum assigned to two cells, to one or None. A face is on the boundary if is is exactly assigned to one cell.

>>> cell_network.face_cells(7)
[12, 8]
>>> cell_network.face_cells(9)
[8]
>>> cell_network.faces_without_cell()
[34, 35, 36, 37, 38, 39]
>>> boundary = cell_network.faces_on_boundaries()
>>> boundary
[1, 2, 3, 5, 9, 10, 11, 13, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 40, 41, 42, 43, 44, 49]

If all cells are connected, those faces form a closed cell as well:

>>> cell_network.do_faces_form_a_closed_cell(boundary)
True

This shows only the faces on the boundary displayed.

.. figure:: /_images/userguide/basics.datastructures.cellnetworks.example_hull.png


If we want to add a cell, we need to provide a list of face keys that form a closed volume.
If they don't, the cell will not be added.

In the following image, the faces belonging to 2 cells are showin in yellow, the faces to one cell are shown in grey, and the faces belonging to no cell are shown in blue.
There is also one edge without face, shown with thicker linewidth.

.. figure:: /_images/userguide/basics.datastructures.cellnetworks.example_color.png




