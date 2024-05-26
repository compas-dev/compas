********************************************************************************
Cell Networks
********************************************************************************

.. rst-class:: lead

A :class:`compas.datastructures.CellNetwork` uses a halfface data structure to represent a collection of mixed topologic entities such as cells, faces, edges and nodes,
and to facilitate the application of topological and geometrical operations on it.
In addition, it provides a number of methods for storing arbitrary data on vertices, edges, faces, cells, and the overall cell network itself.

.. note::

    Please refer to the API for a complete overview of all functionality:

    * :class:`compas.datastructures.CellNetwork`


CellNetwork Construction
=================

Meshes can be constructed in a number of ways:

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

>>> from compas.datastructures import CellNetwork
>>> from compas.scene import Scene
>>> cell_network = CellNetwork.from_json(compas.get('tubemesh.obj'))
>>> scene = Scene()
>>> scene.add(mesh)
>>> scene.show()







