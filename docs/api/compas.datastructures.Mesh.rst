******************************************************************************
Mesh
******************************************************************************

.. currentmodule:: compas.datastructures

.. autoclass:: Mesh

Methods
=======

Constructors
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.from_json
    ~Mesh.from_lines
    ~Mesh.from_meshgrid
    ~Mesh.from_obj
    ~Mesh.from_off
    ~Mesh.from_ply
    ~Mesh.from_points
    ~Mesh.from_polygons
    ~Mesh.from_polyhedron
    ~Mesh.from_polylines
    ~Mesh.from_shape
    ~Mesh.from_stl
    ~Mesh.from_vertices_and_faces

Conversions
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.to_json
    ~Mesh.to_lines
    ~Mesh.to_obj
    ~Mesh.to_off
    ~Mesh.to_ply
    ~Mesh.to_points
    ~Mesh.to_polygons
    ~Mesh.to_polylines
    ~Mesh.to_stl
    ~Mesh.to_vertices_and_faces

Builders and Modifiers
----------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.add_face
    ~Mesh.add_vertex
    ~Mesh.collapse_edge
    ~Mesh.delete_face
    ~Mesh.delete_vertex
    ~Mesh.flip_cycles
    ~Mesh.insert_vertex
    ~Mesh.join
    ~Mesh.merge_faces
    ~Mesh.quads_to_triangles
    ~Mesh.remove_duplicate_vertices
    ~Mesh.remove_unused_vertices
    ~Mesh.split_edge
    ~Mesh.split_face
    ~Mesh.unify_cycles
    ~Mesh.unweld_edges
    ~Mesh.unweld_vertices
    ~Mesh.weld

Accessors
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.edge_sample
    ~Mesh.edges
    ~Mesh.edges_on_boundaries
    ~Mesh.edges_on_boundary
    ~Mesh.edges_where
    ~Mesh.edges_where_predicate
    ~Mesh.face_sample
    ~Mesh.faces
    ~Mesh.faces_on_boundaries
    ~Mesh.faces_on_boundary
    ~Mesh.faces_where
    ~Mesh.faces_where_predicate
    ~Mesh.vertex_sample
    ~Mesh.vertices
    ~Mesh.vertices_on_boundaries
    ~Mesh.vertices_on_boundary
    ~Mesh.vertices_where
    ~Mesh.vertices_where_predicate

Attributes
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.edge_attribute
    ~Mesh.edge_attributes
    ~Mesh.edges_attribute
    ~Mesh.edges_attributes
    ~Mesh.face_attribute
    ~Mesh.face_attributes
    ~Mesh.faces_attribute
    ~Mesh.faces_attributes
    ~Mesh.vertex_attribute
    ~Mesh.vertex_attributes
    ~Mesh.vertices_attribute
    ~Mesh.vertices_attributes
    ~Mesh.update_default_edge_attributes
    ~Mesh.update_default_face_attributes
    ~Mesh.update_default_vertex_attributes
    ~Mesh.unset_edge_attribute
    ~Mesh.unset_face_attribute
    ~Mesh.unset_vertex_attribute

Topology
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.connected_vertices
    ~Mesh.connected_faces
    ~Mesh.edge_faces
    ~Mesh.edge_loop
    ~Mesh.edge_strip
    ~Mesh.euler
    ~Mesh.face_adjacency_halfedge
    ~Mesh.face_adjacency_vertices
    ~Mesh.face_corners
    ~Mesh.face_degree
    ~Mesh.face_halfedges
    ~Mesh.face_max_degree
    ~Mesh.face_min_degree
    ~Mesh.face_neighbors
    ~Mesh.face_neighborhood
    ~Mesh.face_vertex_ancestor
    ~Mesh.face_vertex_descendant
    ~Mesh.face_vertices
    ~Mesh.halfedge_after
    ~Mesh.halfedge_before
    ~Mesh.halfedge_face
    ~Mesh.halfedge_loop
    ~Mesh.halfedge_loop_vertices
    ~Mesh.halfedge_strip
    ~Mesh.halfedge_strip_faces
    ~Mesh.has_edge
    ~Mesh.has_face
    ~Mesh.has_halfedge
    ~Mesh.has_vertex
    ~Mesh.is_closed
    ~Mesh.is_connected
    ~Mesh.is_edge_on_boundary
    ~Mesh.is_empty
    ~Mesh.is_face_on_boundary
    ~Mesh.is_manifold
    ~Mesh.is_orientable
    ~Mesh.is_quadmesh
    ~Mesh.is_regular
    ~Mesh.is_trimesh
    ~Mesh.is_valid
    ~Mesh.is_vertex_connected
    ~Mesh.is_vertex_on_boundary
    ~Mesh.number_of_edges
    ~Mesh.number_of_faces
    ~Mesh.number_of_vertices
    ~Mesh.vertex_degree
    ~Mesh.vertex_edges
    ~Mesh.vertex_faces
    ~Mesh.vertex_max_degree
    ~Mesh.vertex_min_degree
    ~Mesh.vertex_neighbors
    ~Mesh.vertex_neighborhood

Geometry
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.aabb
    ~Mesh.area
    ~Mesh.centroid
    ~Mesh.edge_coordinates
    ~Mesh.edge_direction
    ~Mesh.edge_end
    ~Mesh.edge_length
    ~Mesh.edge_line
    ~Mesh.edge_midpoint
    ~Mesh.edge_point
    ~Mesh.edge_start
    ~Mesh.edge_vector
    ~Mesh.face_area
    ~Mesh.face_aspect_ratio
    ~Mesh.face_center
    ~Mesh.face_centroid
    ~Mesh.face_circle
    ~Mesh.face_coordinates
    ~Mesh.face_curvature
    ~Mesh.face_flatness
    ~Mesh.face_frame
    ~Mesh.face_normal
    ~Mesh.face_plane
    ~Mesh.face_points
    ~Mesh.face_polygon
    ~Mesh.face_skewness
    ~Mesh.normal
    ~Mesh.obb
    ~Mesh.vertex_area
    ~Mesh.vertex_coordinates
    ~Mesh.vertex_curvature
    ~Mesh.vertex_point
    ~Mesh.vertex_laplacian
    ~Mesh.vertex_neighborhood_centroid
    ~Mesh.vertex_normal
    ~Mesh.vertices_points
    ~Mesh.set_vertex_point
    ~Mesh.smooth_area
    ~Mesh.smooth_centroid
    ~Mesh.transform
    ~Mesh.transformed

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

    ~Mesh.adjacency_matrix
    ~Mesh.connectivity_matrix
    ~Mesh.degree_matrix
    ~Mesh.face_matrix
    ~Mesh.laplacian_matrix

Mappings
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.gkey_vertex
    ~Mesh.vertex_gkey
    ~Mesh.vertex_index
    ~Mesh.index_vertex

Utilities
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.summary
    ~Mesh.copy
    ~Mesh.clear

Other
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Mesh.dual
    ~Mesh.exploded
    ~Mesh.offset
    ~Mesh.subdivided
    ~Mesh.thickened
