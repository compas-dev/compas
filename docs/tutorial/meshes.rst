.. _working-with-meshes:

*******************
Working with meshes
*******************

.. highlight:: python

COMPAS meshes are polygon meshes with support for n-sided polygonal
faces. The meshes are presented using a half-edge data structure. In a
half-edge data structure, each edge is composed of two half-edges with
opposite orientation. Each half-edge is part of exactly one face, unless
it is on the boundary. An edge is thus incident to at least one face and
at most to two. The half-edges of a face form a continuous cycle,
connecting the vertices of the face in a specific order forming a closed
n-sided polygon. The ordering of the vertices determines the direction
of its normal.

Check out the docs for detailed information about the mesh and the available
functionality: :class:`compas.datastructures.Mesh`.


Building a Mesh
===============

Meshes can be built from scratch by adding vertices and faces.::

    >>> from compas.datastrctures import Mesh

    >>> mesh = Mesh()

    >>> a = mesh.add_vertex()  # x,y,z coordinates are optional and default to 0,0,0
    >>> b = mesh.add_vertex(x=1)
    >>> c = mesh.add_vertex(x=1, y=1)
    >>> d = mesh.add_vertex(y=1)

    >>> mesh.add_face([a, b, c, d])


Constructors
============

Building a mesh vertex per vertex and face per face is fine for very simple meshes,
but quickly becomes tedious for meshes of relevant size.
Alternative constructors can be used to simplify this process based on specific inputs.::

    >>> mesh = Mesh.from_vertices_and_faces(vertices, faces)
    >>> mesh = Mesh.from_polygons(polygons)
    >>> mesh = Mesh.from_shape(box)

For strictly two-dimensional inputs in the XY plane, the following can also be used.::

    >>> mesh = Mesh.from_lines(lines)
    >>> mesh = Mesh.from_points(points)

``from_lines`` uses a wall-follower to find the faces of the connected lines.
This process is only successful if the input lines form a planar graph.
``from_points`` generates a delaunay triangulation of the provided points in the XY plane.

For every ``from_`` function there is a corresponding ``to_`` function that basically accomplishes the exact opposite.::

    >>>


Geometry Formats
================

The mesh also supports constructors based on common geometry formats for 3D polygon mesh geometry.::

    >>> mesh = Mesh.from_obj(filepath)
    >>> mesh = Mesh.from_off(filepath)
    >>> mesh = Mesh.from_ply(filepath)
    >>> mesh = Mesh.from_stl(filepath)

As mentioned above, for every ``from_`` there is a ``to_``.::

    >>> mesh = Mesh.from_obj(filepath)
    >>> mesh = Mesh.from_off(filepath)
    >>> mesh = Mesh.from_ply(filepath)
    >>> mesh = Mesh.from_stl(filepath)


Vertices, Faces, Edges
======================

To access the vertices, faces, and edges of the mesh data structure, use the corresponding methods.
Note that these methods return generator objects that have to be consumed by iteration.

::

    >>> mesh.vertices()
    <generator object HalfEdge.vertices at 0x7fe3cb20f4a0>

    >>> mesh.faces()
    <generator object HalfEdge.faces at 0x7fe3cb20f4a0>

    >>> mesh.edges()
    <generator object HalfEdge.edges at 0x7fe3cb20f510>

::

    >>> for vertex in mesh.vertices():
    ...     print(vertex)
    ...

    >>> for face in mesh.faces():
    ...     print(face)
    ...

    >>> for edge in mesh.edges():
    ...     print(edge)
    ...

To obtain actual lists of components, the results from the accessor functions have to be converted explicitly.::

    >>> vertices = list(mesh.vertices())
    >>> edges = list(mesh.edges())
    >>> faces = list(mesh.faces())

The items returned by the accessor methods are identifiers that are unique in the context of the particular component.
Identifiers of vertices and faces are positive integers, including zero.
Identifiers of edges are pairs of vertex ids in the form of a tuple.

Note that adding and removing elements will not cause identifiers to be renumbered.
Therefore, after certain topological operations (e.g. subdivision), vertex and face identifiers no longer necessarily form contiguous sequences.
This needs to be taken into account when converting sequences of vertices, faces, and edges to lists, for example for numerical calculation.
To transparently convert non-contiguous sequences of identifiers to contiguous list indices, use "key/index maps".::

    >>> key_index = mesh.key_index()
    >>> vertices = list(mesh.vertices())
    >>> edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]
    >>> faces = [[key_index[key] for key in mesh.face_vertices(face)] for face in mesh.faces()]

The key/index map simply maps vertex identifiers to the corresponding index in the contiguous sequence that is created
when convertig a sequence of identifiers to a list. The ordering of these identifiers can be completely random, but is always consistent.::

    >>> key_index = {key: index for index, key in enumerate(mesh.vertices())}


Topology
========

Through its half-edge dtaa structure, a mesh can answer several topological questions
about itself and its components.


::

    >>> mesh.vertex_neighbors(vertex, ordered=False)
    >>> mesh.vertex_degree(vertex)
    >>> mesh.vertex_faces(vertex, ordered=False)
    >>> mesh.vertex_neigborhood(vertex, ring=1)
    >>> mesh.vertex_edges(vertex, directed=False)

::

    >>> mesh.face_vertices(face)
    >>> mesh.face_halfedges(face)
    >>> mesh.face_neighbors(face)
    >>> mesh.face_degree(face)

::

    >>> mesh.halfedge_adjacent_face(edge)
    >>> mesh.halfedge_opposite_face(edge)
    >>> mesh.halfedge_next(edge)
    >>> mesh.halfedge_prev(edge)


Geometry
========

::

    >>> mesh.vertex_coordinates(vertex)
    >>> mesh.vertex_normal(vertex)
    >>> mesh.vertex_laplacian(vertex)

::

    >>> mesh.face_centroid(face)
    >>> mesh.face_normal(face)
    >>> mesh.face_plane(face)
    >>> mesh.face_frame(face)
    >>> mesh.face_area(face)

::

    >>> mesh.edge_length(edge)
    >>> mesh.edge_vector(edge)
    >>> mesh.edge_direction(edge)
    >>> mesh.edge_midpoint(edge)
    >>> mesh.edge_point(edge, t=0.0)


Attributes
==========

::

    >>> mesh.vertex_attribute(vertex, 'x')
    >>> mesh.vertex_attributes(vertex, 'xyz')
    >>> mesh.vertices_attribute('z', keys=None)
    >>> mesh.vertices_attributes('xyz', keys=None)

::

    >>> mesh.edge_attribute(edge, 'force')
    >>> mesh.edges_attribute(edge, 'force')


Selections
==========

::

    >>> mesh.vertices_where({'x': 1.0, 'y': (0.0, 10.0)})

::

    >>> a = mesh.vertices_where({'x': 1})
    >>> b = mesh.vertices_where({'x': (5, 10)})
    >>> list(set(a + b))


Serialization
=============


Algorithms
==========



Plugins
=======
