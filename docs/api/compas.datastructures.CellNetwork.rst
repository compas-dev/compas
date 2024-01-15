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
    ~CellNetwork.to_json
    ~CellNetwork.to_network
    ~CellNetwork.mesh_from_faces


Builders and Modifiers
----------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.add_cell
    ~CellNetwork.add_edge
    ~CellNetwork.add_halfface
    ~CellNetwork.add_vertex
    ~CellNetwork.delete_cell
    ~CellNetwork.delete_vertex
    ~CellNetwork.remove_unused_vertices


Accessors
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_sample
    ~CellNetwork.cells
    ~CellNetwork.cells_on_boundaries
    ~CellNetwork.cells_where
    ~CellNetwork.cells_where_predicate
    ~CellNetwork.edge_sample
    ~CellNetwork.edges
    ~CellNetwork.edges_no_face
    ~CellNetwork.edges_where
    ~CellNetwork.edges_where_predicate
    ~CellNetwork.face_sample
    ~CellNetwork.faces
    ~CellNetwork.faces_no_cell
    ~CellNetwork.faces_on_boundaries
    ~CellNetwork.faces_where
    ~CellNetwork.faces_where_predicate
    ~CellNetwork.halffaces
    ~CellNetwork.halffaces_on_boundaries
    ~CellNetwork.non_manifold_edges
    ~CellNetwork.vertex_sample
    ~CellNetwork.vertices
    ~CellNetwork.vertices_on_boundaries
    ~CellNetwork.vertices_where
    ~CellNetwork.vertices_where_predicate


Attributes
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_attribute
    ~CellNetwork.cell_attributes
    ~CellNetwork.cells_attribute
    ~CellNetwork.cells_attributes
    ~CellNetwork.edge_attribute
    ~CellNetwork.edge_attributes
    ~CellNetwork.edges_attribute
    ~CellNetwork.edges_attributes
    ~CellNetwork.face_attribute
    ~CellNetwork.face_attributes
    ~CellNetwork.faces_attribute
    ~CellNetwork.faces_attributes
    ~CellNetwork.vertex_attribute
    ~CellNetwork.vertex_attributes
    ~CellNetwork.vertices_attribute
    ~CellNetwork.vertices_attributes
    ~CellNetwork.update_default_cell_attributes
    ~CellNetwork.update_default_edge_attributes
    ~CellNetwork.update_default_face_attributes
    ~CellNetwork.update_default_vertex_attributes
    ~CellNetwork.unset_cell_attribute
    ~CellNetwork.unset_edge_attribute
    ~CellNetwork.unset_face_attribute
    ~CellNetwork.unset_vertex_attribute


Topology
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_edges
    ~CellNetwork.cell_face_neighbors
    ~CellNetwork.cell_faces
    ~CellNetwork.cell_halfedge_face
    ~CellNetwork.cell_halfedge_opposite_face
    ~CellNetwork.cell_halfedges
    ~CellNetwork.cell_neighbors
    ~CellNetwork.cell_vertex_faces
    ~CellNetwork.cell_vertex_neighbors
    ~CellNetwork.cell_vertices
    ~CellNetwork.edge_cells
    ~CellNetwork.edge_face_adjacency
    ~CellNetwork.edge_faces
    ~CellNetwork.face_adjacency
    ~CellNetwork.edge_halffaces
    ~CellNetwork.face_cells
    ~CellNetwork.face_cell_adjacency
    ~CellNetwork.face_edges
    ~CellNetwork.face_neighbors
    ~CellNetwork.halfface_cell
    ~CellNetwork.halfface_adjacent_halfface
    ~CellNetwork.halfface_halfedges
    ~CellNetwork.halfface_manifold_neighbors
    ~CellNetwork.halfface_manifold_neighborhood
    ~CellNetwork.halfface_opposite_cell
    ~CellNetwork.halfface_opposite_halfface
    ~CellNetwork.halfface_vertex_ancestor
    ~CellNetwork.halfface_vertex_descendent
    ~CellNetwork.halfface_vertices
    ~CellNetwork.has_edge
    ~CellNetwork.has_halfface
    ~CellNetwork.has_vertex
    ~CellNetwork.is_cell_on_boundary
    ~CellNetwork.is_edge_on_boundary
    ~CellNetwork.is_halfface_on_boundary
    ~CellNetwork.is_valid
    ~CellNetwork.is_vertex_on_boundary
    ~CellNetwork.number_of_cells
    ~CellNetwork.number_of_edges
    ~CellNetwork.number_of_faces
    ~CellNetwork.number_of_vertices
    ~CellNetwork.vertex_cells
    ~CellNetwork.vertex_degree
    ~CellNetwork.vertex_halffaces
    ~CellNetwork.vertex_max_degree
    ~CellNetwork.vertex_min_degree
    ~CellNetwork.vertex_neighbors
    ~CellNetwork.vertex_neighborhood


Geometry
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~CellNetwork.cell_center
    ~CellNetwork.cell_centroid
    ~CellNetwork.cell_points
    ~CellNetwork.cell_polyhedron
    ~CellNetwork.cell_vertex_normal
    ~CellNetwork.edge_direction
    ~CellNetwork.edge_end
    ~CellNetwork.edge_length
    ~CellNetwork.edge_line
    ~CellNetwork.edge_vector
    ~CellNetwork.edge_start
    ~CellNetwork.face_area
    ~CellNetwork.face_center
    ~CellNetwork.face_centroid
    ~CellNetwork.face_coordinates
    ~CellNetwork.face_normal
    ~CellNetwork.face_points
    ~CellNetwork.face_polygon
    ~CellNetwork.vertex_coordinates
    ~CellNetwork.vertex_point
    ~CellNetwork.vertices_coordinates
    ~CellNetwork.vertices_points


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

