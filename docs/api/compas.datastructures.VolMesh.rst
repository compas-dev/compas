******************************************************************************
VolMesh
******************************************************************************

.. currentmodule:: compas.datastructures

.. autoclass:: VolMesh

Methods
=======

Constructors
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.from_json
    ~VolMesh.from_obj
    ~VolMesh.from_vertices_and_cells


Conversions
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.cell_to_mesh
    ~VolMesh.cell_to_vertices_and_faces
    ~VolMesh.to_json
    ~VolMesh.to_obj
    ~VolMesh.to_vertices_and_cells


Builders and Modifiers
----------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.add_cell
    ~VolMesh.add_halfface
    ~VolMesh.add_vertex
    ~VolMesh.delete_cell
    ~VolMesh.delete_vertex
    ~VolMesh.remove_unused_vertices


Accessors
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.cell_sample
    ~VolMesh.cells
    ~VolMesh.cells_on_boundaries
    ~VolMesh.cells_where
    ~VolMesh.cells_where_predicate
    ~VolMesh.edge_sample
    ~VolMesh.edges
    ~VolMesh.edges_where
    ~VolMesh.edges_where_predicate
    ~VolMesh.face_sample
    ~VolMesh.faces
    ~VolMesh.faces_where
    ~VolMesh.faces_where_predicate
    ~VolMesh.halffaces
    ~VolMesh.halffaces_on_boundaries
    ~VolMesh.vertex_sample
    ~VolMesh.vertices
    ~VolMesh.vertices_on_boundaries
    ~VolMesh.vertices_where
    ~VolMesh.vertices_where_predicate


Attributes
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.cell_attribute
    ~VolMesh.cell_attributes
    ~VolMesh.cells_attribute
    ~VolMesh.cells_attributes
    ~VolMesh.edge_attribute
    ~VolMesh.edge_attributes
    ~VolMesh.edges_attribute
    ~VolMesh.edges_attributes
    ~VolMesh.face_attribute
    ~VolMesh.face_attributes
    ~VolMesh.faces_attribute
    ~VolMesh.faces_attributes
    ~VolMesh.vertex_attribute
    ~VolMesh.vertex_attributes
    ~VolMesh.vertices_attribute
    ~VolMesh.vertices_attributes
    ~VolMesh.update_default_cell_attributes
    ~VolMesh.update_default_edge_attributes
    ~VolMesh.update_default_face_attributes
    ~VolMesh.update_default_vertex_attributes
    ~VolMesh.unset_cell_attribute
    ~VolMesh.unset_edge_attribute
    ~VolMesh.unset_face_attribute
    ~VolMesh.unset_vertex_attribute


Topology
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.cell_edges
    ~VolMesh.cell_face_neighbors
    ~VolMesh.cell_faces
    ~VolMesh.cell_halfedge_face
    ~VolMesh.cell_halfedge_opposite_face
    ~VolMesh.cell_halfedges
    ~VolMesh.cell_neighbors
    ~VolMesh.cell_vertex_faces
    ~VolMesh.cell_vertex_neighbors
    ~VolMesh.cell_vertices
    ~VolMesh.edge_cells
    ~VolMesh.edge_halffaces
    ~VolMesh.halfface_cell
    ~VolMesh.halfface_adjacent_halfface
    ~VolMesh.halfface_halfedges
    ~VolMesh.halfface_manifold_neighbors
    ~VolMesh.halfface_manifold_neighborhood
    ~VolMesh.halfface_opposite_cell
    ~VolMesh.halfface_opposite_halfface
    ~VolMesh.halfface_vertex_ancestor
    ~VolMesh.halfface_vertex_descendent
    ~VolMesh.halfface_vertices
    ~VolMesh.has_edge
    ~VolMesh.has_halfface
    ~VolMesh.has_vertex
    ~VolMesh.is_cell_on_boundary
    ~VolMesh.is_edge_on_boundary
    ~VolMesh.is_halfface_on_boundary
    ~VolMesh.is_valid
    ~VolMesh.is_vertex_on_boundary
    ~VolMesh.number_of_cells
    ~VolMesh.number_of_edges
    ~VolMesh.number_of_faces
    ~VolMesh.number_of_vertices
    ~VolMesh.vertex_cells
    ~VolMesh.vertex_degree
    ~VolMesh.vertex_halffaces
    ~VolMesh.vertex_max_degree
    ~VolMesh.vertex_min_degree
    ~VolMesh.vertex_neighbors
    ~VolMesh.vertex_neighborhood


Geometry
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.cell_center
    ~VolMesh.cell_centroid
    ~VolMesh.cell_points
    ~VolMesh.cell_polyhedron
    ~VolMesh.cell_vertex_normal
    ~VolMesh.edge_direction
    ~VolMesh.edge_end
    ~VolMesh.edge_length
    ~VolMesh.edge_line
    ~VolMesh.edge_vector
    ~VolMesh.edge_start
    ~VolMesh.face_area
    ~VolMesh.face_center
    ~VolMesh.face_centroid
    ~VolMesh.face_coordinates
    ~VolMesh.face_normal
    ~VolMesh.face_points
    ~VolMesh.face_polygon
    ~VolMesh.vertex_coordinates
    ~VolMesh.vertex_point


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

    ~VolMesh.gkey_vertex
    ~VolMesh.index_vertex
    ~VolMesh.vertex_gkey
    ~VolMesh.vertex_index


Utilities
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~VolMesh.clear
    ~VolMesh.copy


Other
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

