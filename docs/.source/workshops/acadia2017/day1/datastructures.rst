.. _acadia2017_day1_datastructures:

********************************************************************************
Datastructures
********************************************************************************

Network, Mesh, VolMesh
======================

The *compas* framework contains three types of data structures and related operations and algorithms:

* :class:`compas.datastructures.Network`
* :class:`compas.datastructures.Mesh`
* :class:`compas.datastructures.VolMesh`

.. images
.. overview

For this tutorial, we will focus on the mesh data structure.

.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices()
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.draw_vertices(
        text='key',
        facecolor=(0.9, 0.9, 0.9),
    )
    plotter.draw_faces(
        text='key',
        facecolor=(0.7, 0.7, 0.7),
    )
    plotter.draw_edges(
        text='key'
    )

    plotter.show()


Construction
============

All datastructures come with factory constructors.
These are implemented as class methods (using the ``@classmethod`` decoreator) and
are named using the following pattern ``.from_xxx``.

.. code-block:: python

    mesh = Mesh.from_data(...)
    mesh = Mesh.from_json(...)
    mesh = Mesh.from_obj(...)
    mesh = Mesh.from_vertices_and_faces(...)
    mesh = Mesh.from_polygons(...)
    mesh = Mesh.from_polyhedron(...)
    mesh = Mesh.from_points(...)

``compas`` also provides basic sample data that can be used together with the constructors.

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


Accessing the data
==================

Every datastructure exposes several functions to access its data.
All of those *accessors* are iterators; they are meant to be iterated over.
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


The same applies to the faces.
The accessor is an iterator; it is meant for iterating over the faces.
To count the faces or to get a list of faces, the iterator needs to be converted
explicitly.

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

The available functions for accessing the topological data depend on the type of
datastructure, although they obviously have a few of them in common.

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
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    root = 17
    nbrs = mesh.vertex_neighbours(root, ordered=True)

    text = {nbr: str(i) for i, nbr in enumerate(nbrs)}
    text[root] = root 

    fcolor = {nbr: '#cccccc' for nbr in nbrs}
    fcolor[root] = '#ff0000'

    plotter.draw_vertices(
        text=text,
        facecolor=fcolor
    )
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()

.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices(text={key: mesh.vertex_degree(key) for key in mesh.vertices()})
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()


Geometry
========

* mesh.vertex_coordinates()
* mesh.vertex_area()
* mesh.vertex_centroid()


* mesh.face_area()
* mesh.face_centroid()
* mesh.face_center()
* mesh.face_frame()
* mesh.face_circle()
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
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices()
    plotter.draw_faces(text={fkey: '%.1f' % mesh.face_area(fkey) for fkey in mesh.faces()})
    plotter.draw_edges()

    plotter.show()

.. plot::
    :include-source:

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices(text={key: '%.1f' % mesh.vertex_area(key) for key in mesh.vertices()})
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.show()


Operations
==========

.. code-block:: python
    
    mesh.delete_vertex
    mesh.insert_vertex
    mesh.delete_face

    compas.datastructures.mesh_collapse_edge
    compas.datastructures.mesh_swap_edge
    compas.datastructures.mesh_split_edge

    compas.datastructures.trimesh_collapse_edge
    compas.datastructures.trimesh_swap_edge
    compas.datastructures.trimesh_split_edge


Algorithms
==========

.. code-block:: python
    
    compas.datastructures.mesh_subdivide
    compas.datastructures.mesh_dual
    compas.datastructures.mesh_delaunay_from_points
    compas.datastructures.mesh_voronoi_from_points

    compas.datastructures.trimesh_remesh

.. code-block:: python
    
    compas.geometry.smooth_centroid
    compas.geometry.smooth_centerofmass
    compas.geometry.smooth_area

.. code-block:: python
    
    compas.geometry.shortest_path
    compas.geometry.dijkstra_path


CAD integration
===============



