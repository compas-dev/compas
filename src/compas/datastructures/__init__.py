"""
.. _compas.datastructures:

********************************************************************************
datastructures
********************************************************************************

.. module:: compas.datastructures


Class definitions of data structures, data structure algorithms and operations.


Network
=======

.. autosummary::
    :toctree: generated/

    Network

.. code-block:: python

    >>> import compas
    >>> from compas.datastructures import Network
    >>> from compas.visualization import NetworkPlotter

    >>> n = Network.from_obj(compas.get_data('grid_irregular.obj'))
    >>> p = NetworkPlotter(n)

    >>> f = {key: '#ff0000' for key in n.leaves()}
    >>> t = {(u, v): '{:.1f}'.format(n.edge_length(u, v)) for u, v in n.edges()}

    >>> p.draw_vertices(facecolor=f)
    >>> p.draw_edges(text=t)
    >>> p.show()

.. plot::

    import compas
    from compas.datastructures import Network
    from compas.visualization import NetworkPlotter
    network = Network.from_obj(compas.get_data('grid_irregular.obj'))
    p = NetworkPlotter(network)
    p.draw_vertices(facecolor={key: '#ff0000' for key in network.leaves()})
    p.draw_edges(text={(u, v): '{:.1f}'.format(network.edge_length(u, v)) for u, v in network.edges() })
    p.show()


network.operations
------------------

.. autosummary::
    :toctree: generated/

    network_split_edge


network.algorithms
------------------

.. autosummary::
    :toctree: generated/

    network_bfs
    network_bfs_paths
    network_count_crossings
    network_dfs
    network_dfs_paths
    network_dijkstra_distances
    network_dijkstra_path
    network_dual
    network_embed_in_plane
    network_find_faces
    network_find_crossings
    network_is_xy
    network_is_crossed
    network_is_planar
    network_is_planar_embedding
    network_shortest_path
    network_smooth_area
    network_smooth_centroid
    network_smooth_length
    network_smooth_mass
    network_smooth_mixed
    network_vertex_coloring


.. plot::
    :include-source:

    import compas

    from compas.datastructures import Network
    from compas.datastructures import network_dijkstra_path

    from compas.visualization import NetworkPlotter

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    # set a very high weight on one of the edges

    weight[(8, 7)] = 1000
    weight[(7, 8)] = 1000

    # define start and end of the path

    start = 21
    end = 22

    path = network_dijkstra_path(network.adjacency, weight, start, end)

    # plot

    edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if v not in network.edge[u]:
            u, v = v, u
        edges.append([u, v])

    plotter = NetworkPlotter(network)

    plotter.draw_vertices(
        text={key: key for key in path},
        facecolor={key: '#ff0000' for key in (path[0], path[-1])},
        radius=0.15
    )

    plotter.draw_edges(
        color={(u, v): '#ff0000' for u, v in edges},
        width={(u, v): 2.0 for u, v in edges},
        text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()}
    )

    plotter.show()


Mesh
====

Package for working with mesh objects.

.. autosummary::
    :toctree: generated/

    Mesh


.. code-block:: python

    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> from compas.visualization import MeshPlotter

    >>> m = Mesh.from_obj(compas.get_data('faces.obj'))
    >>> p = MeshPlotter(m)

    >>> p.defaults['face.facecolor'] = '#eeeeee'
    >>> f = {key: '#00ff00' for key in mesh.vertices_on_boundary()}
    >>> t = {fkey: str(fkey) for fkey in mesh.faces()}

    >>> p.draw_vertices(facecolor=f)
    >>> p.draw_faces(text=t)
    >>> p.show()

.. plot::
    :class: figure-img img-fluid

    import compas
    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter
    mesh = Mesh.from_obj(compas.get_data('faces.obj'))
    p = MeshPlotter(mesh)
    p.defaults['face.facecolor'] = '#eeeeee'
    p.draw_vertices(facecolor={key: '#00ff00' for key in mesh.vertices_on_boundary()})
    p.draw_faces(text={fkey: str(fkey) for fkey in mesh.faces()})
    p.show()


mesh.operations
---------------

.. autosummary::
    :toctree: generated/

    mesh_collapse_edge
    mesh_insert_edge
    mesh_split_edge
    mesh_split_face
    mesh_unweld_vertices


.. autosummary::
    :toctree: generated/

    trimesh_collapse_edge
    trimesh_split_edge
    trimesh_swap_edge


mesh.algorithms
---------------

.. autosummary::
    :toctree: generated/

    mesh_circularize
    mesh_delaunay_from_points
    mesh_dual
    mesh_flip_cycles
    mesh_planarize
    mesh_smooth_centroid
    mesh_smooth_centerofmass
    mesh_smooth_length
    mesh_smooth_area
    mesh_smooth_angle
    mesh_subdivide
    mesh_subdivide_tri
    mesh_subdivide_catmullclark
    mesh_subdivide_doosabin
    mesh_unify_cycles
    mesh_voronoi_from_points


.. autosummary::
    :toctree: generated/

    trimesh_optimise_topology
    trimesh_subdivide_loop


VolMesh
=======

.. code-block:: python

    >>> import compas
    >>> from compas.datastructures import VolMesh

    >>> m = VolMesh.from_obj(compas.get_data('boxes.obj'))


volmesh.operations
------------------


volmesh.algorithms
------------------


"""

from __future__ import print_function

from .network import *
from .mesh import *
from .volmesh import *

from .network import __all__ as a
from .mesh import __all__ as b
from .volmesh import __all__ as c

__all__ = a + b + c
