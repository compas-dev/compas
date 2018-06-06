********************************************************************************
Working with datastructures
********************************************************************************

.. vertex identifiers are integers by default
.. any other hashable type may be used
.. ordering of vertices is unknown, but constant, unless changes are made to the structure of the data
.. iterators v lists
.. data v attributes

.. oragnise as facts v details

.. link to algorithms / relation to algorithms
.. link to numerical / relation to numerical


Network, Mesh, VolMesh
======================

.. currentmodule:: compas.datastructures

The main library of the **COMPAS** framework contains three fundamental data structures:

* :class:`Network`
* :class:`Mesh`
* :class:`VolMesh`

These can be used as-is, but they can also be easily extended or combined to form
entirely different data structures. For this tutorial, we will use the mesh
data structure to demonstrate the general principles and give an overview of the
possibilities.

.. figure:: /_images/datastructures.png
    :figclass: figure
    :class: figure-img img-fluid


Construction
============

All datastructures come with factory constructors. These are implemented as class
methods (using the ``@classmethod`` decoreator) and are named using the following
pattern ``.from_xxx``.

.. code-block:: python

    mesh = Mesh.from_data(...)
    mesh = Mesh.from_json(...)
    mesh = Mesh.from_obj(...)
    mesh = Mesh.from_vertices_and_faces(...)
    mesh = Mesh.from_polygons(...)
    mesh = Mesh.from_polyhedron(...)
    mesh = Mesh.from_points(...)

`compas` also provides sample data that can be used together with the constructors,
for example for debugging or to generate example code.

.. code-block:: python

    from __future__ import print_function
    
    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    print(mesh)

    # ================================================================================
    # Mesh summary
    # ================================================================================
    #
    # - name: Mesh
    # - vertices: 36
    # - edges: 60
    # - faces: 25
    # - vertex degree: 2/4
    # - face degree: 2/4
    #
    # ================================================================================

Printing the mesh produces a summary of the mesh's properties:
the number of vertices, edges and faces and information about vertex and face degree.


Data
====

All data *accessors* are iterators; they are meant to be iterated over.
Lists of data have to be constructed explicitly.

* mesh.vertices()
* mesh.faces()
* mesh.halfedges()
* mesh.edges()

.. code-block:: python

    from __future__ import print_function

    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    for key in mesh.vertices():
        print(key)

    for key, attr in mesh.vertices(True):
        print(key, attr)

    print(list(mesh.vertices()))
    print(mesh.number_of_vertices())


.. code-block:: python
    
    from __future__ import print_function

    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    for fkey in mesh.faces():
        print(fkey)

    for fkey, attr in mesh.faces(True):
        print(fkey, attr)

    print(len(list(mesh.faces()))
    print(mesh.number_of_faces())


Topology
========

* mesh.is_valid()
* mesh.is_regular()
* mesh.is_connected()
* mesh.is_manifold()
* mesh.is_orientable()
* mesh.is_trimesh()
* mesh.is_quadmesh()

* mesh.vertex_neighbours()
* mesh.vertex_degree()
* mesh.vertex_faces()
* mesh.vertex_neighbourhood()

* mesh.face_vertices()
* mesh.face_halfedges()
* mesh.face_neighbours()
* mesh.face_neighbourhood()
* mesh.face_vertex_ancestor()
* mesh.face_vertex_descendant()


.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    root = 17
    nbrs = mesh.vertex_neighbours(root, ordered=True)

    text = {nbr: str(i) for i, nbr in enumerate(nbrs)}
    text[root] = root 

    facecolor = {nbr: '#cccccc' for nbr in nbrs}
    facecolor[root] = '#ff0000'

    plotter.draw_vertices(
        text=text,
        facecolor=facecolor,
        radius=0.15
    )
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()


Geometry
========

* mesh.vertex_coordinates()
* mesh.vertex_area()
* mesh.vertex_centroid()
* mesh.vertex_normal()

* mesh.face_coordinates()
* mesh.face_area()
* mesh.face_centroid()
* mesh.face_center()
* mesh.face_normal()
* mesh.face_flatness()

* mesh.edge_coordinates()
* mesh.edge_vector()
* mesh.edge_direction()
* mesh.edge_length()
* mesh.edge_midpoint()


.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices()
    plotter.draw_faces(text={fkey: '%.1f' % mesh.face_area(fkey) for fkey in mesh.faces()})
    plotter.draw_edges()

    plotter.show()

