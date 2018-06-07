********************************************************************************
Working with datastructures
********************************************************************************

.. vertex identifiers are integers by default
.. any other hashable type may be used
.. ordering of vertices is unknown, but constant, unless changes are made to the structure of the data
.. iterators v lists
.. data v attributes

.. oragnise as facts v details

.. add assembly and diagram?
.. or split up into separate tutorials?


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


Access
======

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


Algorithms
==========

* :func:`compas.topology.trimesh_remesh`

.. code-block:: python

    # mesh remeshing
    
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    from compas.topology import trimesh_remesh


    # make a square
    # and insert a vertex in the middle
    # to create a triangle mesh

    vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (10.0, 10.0, 0.0), (0.0, 10.0, 0.0)]
    faces = [[0, 1, 2, 3]]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    mesh.insert_vertex(0)


    # create a plotter for visualization
    # draw the initial mesh as edges
    # define a callback to update the edges during the algorithm

    plotter = MeshPlotter(mesh)

    plotter.draw_edges()

    def callback(mesh, k, args):
        plotter.update_edges()
        plotter.update(pause=0.001)


    # run the remeshing algorithm
    # visualize the end result
    # with faces and edges

    trimesh_remesh(
        mesh,
        0.5,
        tol=0.02,
        kmax=500,
        allow_boundary_split=True,
        allow_boundary_swap=True,
        allow_boundary_collapse=False,
        fixed=mesh.vertices_on_boundary(),
        callback=callback)

    plotter.clear_edges()
    plotter.update()

    plotter.draw_faces()
    plotter.draw_edges()
    plotter.update()

    plotter.show()


* :func:`compas.topology.trimesh_remesh`
* :func:`compas.topology.delaunay_from_points`
* :func:`compas.topology.voronoi_from_delaunay`

.. code-block:: python

    # delaunay and voronoi

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    from compas.topology import trimesh_remesh
    from compas.topology import delaunay_from_points
    from compas.topology import voronoi_from_delaunay

    from compas.geometry import pointcloud_xy


    # create a 2D pointcloud
    # and generate a delaunay triangulation from it
    # remesh the triagulation
    # to give it a more even distribution of edges
    # extract the points
    # and generate the delaunay again
    # generate a voronoi from that delaunay

    points   = pointcloud_xy(10, (0, 10))
    delaunay = delaunay_from_points(Mesh, points)

    trimesh_remesh(delaunay, 1.0, kmax=300, allow_boundary_split=True)

    points   = [delaunay.vertex_coordinates(key) for key in delaunay.vertices()]
    delaunay = delaunay_from_points(Mesh, points)
    voronoi  = voronoi_from_delaunay(delaunay)


    # make a plotter for visualization
    # draw the voronoi as lines
    # on top of the delaunay

    plotter = MeshPlotter(delaunay, figsize=(10, 6))

    lines = []
    for u, v in voronoi.edges():
        lines.append({
            'start': voronoi.vertex_coordinates(u, 'xy'),
            'end'  : voronoi.vertex_coordinates(v, 'xy'),
            'width': 1.0
        })

    plotter.draw_lines(lines)

    plotter.draw_vertices(
        radius=0.075,
        facecolor={key: '#0092d2' for key in delaunay.vertices() if key not in delaunay.vertices_on_boundary()}
    )

    plotter.draw_edges(color='#cccccc')

    plotter.show()


* :func:`compas.topology.dijkstra_path`

.. code-block:: python

    # shortest path

    import compas

    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter

    from compas.topology import dijkstra_path


    # make a network from an irregular grid of lines
    # extract an adjacency dictionary
    # set the weight of each edge equal to its length

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

    weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    # make a few edges heavier
    # for example to simulate traffic problems

    # heavy = [(7, 17), (9, 19)]

    # for u, v in heavy:
    #     weight[(u, v)] = 1000.0
    #     weight[(v, u)] = 1000.0


    # make an interactive plotter
    # for finding shortest paths from a given start to a given end
    # and through an additional user-selected point

    plotter = NetworkPlotter(network, figsize=(10, 8), fontsize=6)


    # choose start and end
    # and set an initial value for the via point

    start = 21
    via = 0
    end = 22


    # define the function that computes the shortest path
    # based on the current via

    def via_via(via):

        # compute the shortest path from start to via
        # and from via to end
        # combine the paths

        path1 = dijkstra_path(adjacency, weight, start, via)
        path2 = dijkstra_path(adjacency, weight, via, end)
        path = path1 + path2[1:]

        edges = []
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            if v not in network.edge[u]:
                u, v = v, u
            edges.append([u, v])


        # update the plot

        vertexcolor = {}
        vertexcolor[start] = '#00ff00'
        vertexcolor[end] = '#00ff00'
        vertexcolor[via] = '#0000ff'

        plotter.clear_vertices()
        plotter.clear_edges()

        plotter.draw_vertices(text={key: key for key in (start, via, end)},
                              textcolor={key: '#ffffff' for key in path[1:-1]},
                              facecolor=vertexcolor,
                              radius=0.15,
                              picker=10)

        plotter.draw_edges(color={(u, v): '#ff0000' for u, v in edges},
                           width={(u, v): 4.0 for u, v in edges},
                           text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()},
                           fontsize=4.0)


    # define a listener for picking points
    # whenever a new point is picked
    # it will call the via_via function
    # with the picked point as via point

    index_key = network.index_key()

    def on_pick(e):
        index = e.ind[0]
        via = index_key[index]
        via_via(via)
        plotter.update()


    # initialize
    # and start

    via_via(via)

    plotter.register_listener(on_pick)
    plotter.show()


Numerical
=========

* :func:`compas.numerical.fd`

.. code-block:: python

    # form finding

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.numerical import fd
    from compas.utilities import i_to_rgb


    # make a mesh from sample data
    # set the default attributes of edges and vertices
    # mark the corners as fixed
    # store the original line geometry for plotting later

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_vertex_attributes({'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_edge_attributes({'q': 1.0})

    for key, attr in mesh.vertices(True):
        attr['is_anchor'] = mesh.vertex_degree(key) == 2

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start' : mesh.vertex_coordinates(u, 'xy'),
            'end'   : mesh.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 1.0
        })


    # process the mesh data
    # into a computation-friendly format
    # i.e. convert everything to lists
    # such that the force density method can convert it into fast Numpy arrays

    k_i   = mesh.key_index()
    xyz   = mesh.get_vertices_attributes(('x', 'y', 'z'))
    loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
    q     = mesh.get_edges_attribute('q')
    fixed = mesh.vertices_where({'is_anchor': True})
    fixed = [k_i[k] for k in fixed]
    edges = [(k_i[u], k_i[v]) for u, v in mesh.edges()]


    # run the force density method
    # update the mesh with the result

    xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads, rtype='list')

    for key, attr in mesh.vertices(True):
        index = k_i[key]
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]

    for index, (u, v, attr) in enumerate(mesh.edges(True)):
        attr['f'] = f[index]


    # make a plotter
    # visualize the original geometry
    # and the equilibrium shape
    # and set the thickness and color of edges
    # proportional to the axial force

    plotter = MeshPlotter(mesh)

    zmax = max(mesh.get_vertices_attribute('z'))
    fmax = max(mesh.get_edges_attribute('f'))

    plotter.draw_lines(lines)

    plotter.draw_vertices()
    plotter.draw_faces()
    plotter.draw_edges(
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in mesh.edges(True)},
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in mesh.edges(True)},
    )

    plotter.show()


CAD integration
===============

* :func:`compas.topology.mesh_subdivide`
* :func:`compas.topology.mesh_subdivide_doosabin`
* :func:`compas.topology.mesh_subdivide_catmullclark`

* :mod:`compas_rhino`

.. code-block:: python

    from compas.datastructures import Mesh
    from compas.topology import mesh_subdivide_doosabin
    from compas.viewers import SubdMeshViewer

    mesh = Mesh.from_polyhedron(6)

    viewer = SubdMeshViewer(mesh, subdfunc=mesh_subdivide_doosabin, width=600, height=600)

    viewer.axes_on = False
    viewer.grid_on = False

    for i in range(10):
        viewer.camera.zoom_in()

    viewer.setup()
    viewer.show()


.. code-block:: python

    from compas.datastructures import Mesh
    from compas.topology import mesh_subdivide_catmullclark

    import compas_rhino

    mesh = Mesh.from_polyhedron(6)
    subd = mesh_subdivide_catmullclark(mesh, k=4)

    compas_rhino.mesh_draw_faces(
        subd,
        join_faces=True
    )


.. code-block:: python

    from __future__ import print_function
    from __future__ import division

    from functools import partial

    import compas_rhino

    from compas.datastructures import Mesh
    from compas.topology import mesh_subdivide


    # make a control mesh

    mesh = Mesh.from_polyhedron(6)


    # give it a name
    # and set default vertex attributes

    mesh.attributes['name'] = 'Control'
    mesh.update_default_vertex_attributes({'is_fixed': False})


    # make a partial function out of compas_rhino.mesh_draw
    # (a function with some of the parameters already filled in)
    # that can be used more easily to redraw the mesh
    # with the same settings in the update loop

    draw = partial(
        compas_rhino.mesh_draw,
        layer='SubdModeling::Control',
        clear_layer=True,
        show_faces=False,
        show_vertices=True,
        show_edges=True)


    # draw the control mesh
    # with showing the faces

    draw(mesh)


    # allow the user to change the attributes of the vertices
    # note: the interaction loop exits
    #       when the user cancels the selection of mesh vertices

    while True:
        keys = compas_rhino.mesh_select_vertices(mesh)
        if not keys:
            break
        compas_rhino.mesh_update_vertex_attributes(mesh, keys)
        draw(mesh, vertexcolor={key: '#ff0000' for key in mesh.vertices_where({'is_fixed': True})})


    # make a subd mesh (using catmullclark)
    # keep the vertices fixed
    # as indicated by the user

    fixed = mesh.vertices_where({'is_fixed': True})
    subd = mesh_subdivide(mesh, scheme='catmullclark', k=5, fixed=fixed)


    # give the mesh a (different) name

    subd.attributes['name'] = 'Mesh'


    # draw the result

    compas_rhino.mesh_draw_faces(
        subd,
        layer='SubdModeling::Mesh',
        clear_layer=True,
        join_faces=True
    )
