.. _acadia2017_day1_datastructures:

********************************************************************************
Datastructures
********************************************************************************

Network, Mesh, VolMesh
======================

The *compas* framework contains three types of data structures and related operations and algorithms:

* ``compas.datastructures.network``
* ``compas.datastructures.mesh``
* ``compas.datastructures.volmesh``

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
    plotter.draw_edges()

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
    
    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    # integer vertex keys: range(0, mesh.number_of_vertices())
    # integer face keys: range(0, mesh.number_of_faces())
    # default vertex attr: {'x': 0.0, 'y': 0.0, 'z': 0.0}
    # default face attr: {}
    # 


Accessing the data
==================

Every datastructure exposes several functions to access its data.
All of those *accessors* are iterators; they are meant to be iterated over.
Lists of data have to be constructed explicitly.

.. code-block:: python

    from __future__ import print_function

    import compas
    from compas.datastructures import Mesh
    mesh = Mesh.from_obj(compas.get('faces.obj'))

    print(mesh)

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

.. code-block:: python

    mesh.vertex_neighbours()
    mesh.vertex_degree()
    mesh.vertex_faces()
    mesh.vertex_neighbourhood()
    ...

    mesh.faces_vertices()
    mesh.face_neighbours()
    mesh.face_neighbourhood()
    ...

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

.. code-block:: python

    mesh.vertex_coordinates()
    mesh.vertex_area()
    mesh.vertex_centroid()
    ...
    mesh.face_area()
    mesh.face_centroid()
    mesh.face_center()
    mesh.face_frame()
    mesh.face_circle()
    mesh.face_normal()
    ...
    mesh.edge_coordinates()
    mesh.edge_vector()
    mesh.edge_direction()
    mesh.edge_length()
    mesh.edge_midpoint()
    ...


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



