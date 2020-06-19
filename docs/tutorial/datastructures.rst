***************
Data structures
***************

.. currentmodule:: compas.datastructures

Why data structures?
====================

Data structures encode relationships between data points.
These data point can be geometrical, or not.
The relationships can be encoded in the form of links or "edges", and loops or "faces".


Data structure types
====================

COMPAS provides three base data structures: :class:`Network`, :class:`Mesh`, :class:`VolMesh`.

:class:`Network` is a "directed edge graph" that encodes the relationships between "nodes" with "edges".
Networks can, for example, be used to keep track of the relationships between the individual elements of a
Discrete Element Assembly, or to represent the elements of a cable net.

For more information, see :ref:`working-with-networks`.

:class:`Mesh` is a "halfedge data structure" that encode relationships between vertices, edges, and faces through
"half-edges" (pairs of vertices that in one direction point to the adjacent face, and in the other direction to the opposite, neighbouring face).
Meshes are ubiquitous in geometry processing, computer graphics, additive manufacturing processes, Finite Element Analysis etc.
COMPAS meshes can represent manifold, open or closed, polygonal surfaces.

For more information, see :ref:`working-with-meshes`.

:class:`VolMesh` is a 3D extension of the essentially 2D poygonal mesh.
In the case of a volumetric mesh or "VolMesh", relationships exist not only between vertices, edges, and faces, but also between cells.
Relationships between cells are encoded with "half-planes" instead of "half-edges".

For more information, see :ref:`working-with-volmeshes`.
