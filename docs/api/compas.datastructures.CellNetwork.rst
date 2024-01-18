******************************************************************************
CellNetwork
******************************************************************************

.. currentmodule:: compas.datastructures

.. autoclass:: CellNetwork

Methods
=======

Constructors
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.from_json


Conversions
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_to_mesh
    ~CellNetwork.cell_to_vertices_and_faces
    ~CellNetwork.edges_to_graph
    ~CellNetwork.faces_to_mesh
    ~CellNetwork.to_json


Builders and Modifiers
----------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.add_cell
    ~CellNetwork.add_edge
    ~CellNetwork.add_face
    ~CellNetwork.add_vertex


General
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.aabb
    ~CellNetwork.centroid
    ~CellNetwork.is_valid
    ~CellNetwork.number_of_cells
    ~CellNetwork.number_of_edges
    ~CellNetwork.number_of_faces
    ~CellNetwork.number_of_vertices


Vertex Accessors
----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.vertex_sample
    ~CellNetwork.vertices
    ~CellNetwork.vertices_where
    ~CellNetwork.vertices_where_predicate


Vertex Attributes
-----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.vertex_attribute
    ~CellNetwork.vertex_attributes
    ~CellNetwork.vertices_attribute
    ~CellNetwork.vertices_attributes
    ~CellNetwork.update_default_vertex_attributes
    ~CellNetwork.unset_vertex_attribute


Vertex Topology
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.has_vertex
    ~CellNetwork.vertex_cells
    ~CellNetwork.vertex_degree
    ~CellNetwork.vertex_faces
    ~CellNetwork.vertex_max_degree
    ~CellNetwork.vertex_min_degree
    ~CellNetwork.vertex_neighbors
    ~CellNetwork.vertex_neighborhood


Vertex Geometry
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.vertex_coordinates
    ~CellNetwork.vertex_point
    ~CellNetwork.vertices_coordinates
    ~CellNetwork.vertices_points


Edge Accessors
--------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.edge_sample
    ~CellNetwork.edges
    ~CellNetwork.edges_where
    ~CellNetwork.edges_where_predicate


Edge Attributes
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.edge_attribute
    ~CellNetwork.edge_attributes
    ~CellNetwork.edges_attribute
    ~CellNetwork.edges_attributes
    ~CellNetwork.update_default_edge_attributes
    ~CellNetwork.unset_edge_attribute


Edge Topology
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.edge_cells
    ~CellNetwork.edge_faces
    ~CellNetwork.has_edge


Edge Geometry
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.edge_direction
    ~CellNetwork.edge_end
    ~CellNetwork.edge_length
    ~CellNetwork.edge_line
    ~CellNetwork.edge_vector
    ~CellNetwork.edge_start


Face Accessors
--------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.face_sample
    ~CellNetwork.faces
    ~CellNetwork.faces_on_boundaries
    ~CellNetwork.faces_where
    ~CellNetwork.faces_where_predicate


Face Attributes
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.face_attribute
    ~CellNetwork.face_attributes
    ~CellNetwork.faces_attribute
    ~CellNetwork.faces_attributes
    ~CellNetwork.update_default_face_attributes
    ~CellNetwork.unset_face_attribute


Face Topology
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.face_cells
    ~CellNetwork.face_edges
    ~CellNetwork.face_vertices
    ~CellNetwork.faces_on_boundaries
    ~CellNetwork.is_face_on_boundary
    ~CellNetwork.isolated_faces


Face Geometry
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.face_area
    ~CellNetwork.face_center
    ~CellNetwork.face_centroid
    ~CellNetwork.face_coordinates
    ~CellNetwork.face_normal
    ~CellNetwork.face_points
    ~CellNetwork.face_polygon


Cell Accessors
--------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_sample
    ~CellNetwork.cells
    ~CellNetwork.cells_on_boundaries
    ~CellNetwork.cells_where
    ~CellNetwork.cells_where_predicate


Cell Attributes
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_attribute
    ~CellNetwork.cell_attributes
    ~CellNetwork.cells_attribute
    ~CellNetwork.cells_attributes
    ~CellNetwork.update_default_cell_attributes
    ~CellNetwork.unset_cell_attribute


Cell Topology
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_edges
    ~CellNetwork.cell_face_halfedges
    ~CellNetwork.cell_face_neighbors
    ~CellNetwork.cell_face_vertices
    ~CellNetwork.cell_faces
    ~CellNetwork.cell_halfedge_face
    ~CellNetwork.cell_halfedges
    ~CellNetwork.cell_vertex_faces
    ~CellNetwork.cell_vertex_neighbors
    ~CellNetwork.cell_vertices
    ~CellNetwork.cells_on_boundaries
    ~CellNetwork.is_cell_on_boundary


Cell Geometry
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_center
    ~CellNetwork.cell_centroid
    ~CellNetwork.cell_points
    ~CellNetwork.cell_polyhedron


Paths
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:


Matrices
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:


Mappings
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.index_vertex
    ~CellNetwork.vertex_index


Utilities
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.clear
    ~CellNetwork.copy


Other
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

