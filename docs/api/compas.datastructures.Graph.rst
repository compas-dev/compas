******************************************************************************
Graph
******************************************************************************

.. currentmodule:: compas.datastructures

.. autoclass:: Graph

Methods
=======

Constructors
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.from_edges
    ~Graph.from_json
    ~Graph.from_lines
    ~Graph.from_networkx
    ~Graph.from_nodes_and_edges
    ~Graph.from_obj
    ~Graph.from_pointcloud

Conversions
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.to_json
    ~Graph.to_lines
    ~Graph.to_networkx
    ~Graph.to_obj
    ~Graph.to_points

Builders and Modifiers
----------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.add_edge
    ~Graph.add_node
    ~Graph.delete_edge
    ~Graph.delete_node
    ~Graph.join_edges
    ~Graph.split_edge

Accessors
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.edge_sample
    ~Graph.edges
    ~Graph.edges_where
    ~Graph.edges_where_predicate
    ~Graph.node_sample
    ~Graph.nodes
    ~Graph.nodes_where
    ~Graph.nodes_where_predicate

Attributes
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.edge_attribute
    ~Graph.edge_attributes
    ~Graph.edges_attribute
    ~Graph.edges_attributes
    ~Graph.node_attribute
    ~Graph.node_attributes
    ~Graph.nodes_attribute
    ~Graph.nodes_attributes
    ~Graph.update_default_edge_attributes
    ~Graph.update_default_node_attributes
    ~Graph.unset_edge_attribute
    ~Graph.unset_node_attribute

Topology
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.complement
    ~Graph.connected_nodes
    ~Graph.connected_edges
    ~Graph.degree
    ~Graph.degree_out
    ~Graph.degree_in
    ~Graph.exploded
    ~Graph.has_edge
    ~Graph.has_node
    ~Graph.is_leaf
    ~Graph.is_node_connected
    ~Graph.neighborhood
    ~Graph.neighbors
    ~Graph.neighbors_in
    ~Graph.neighbors_out
    ~Graph.node_edges
    ~Graph.number_of_edges
    ~Graph.number_of_nodes

Geometry
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.edge_coordinates
    ~Graph.edge_direction
    ~Graph.edge_end
    ~Graph.edge_length
    ~Graph.edge_line
    ~Graph.edge_midpoint
    ~Graph.edge_point
    ~Graph.edge_start
    ~Graph.edge_vector
    ~Graph.node_coordinates
    ~Graph.node_point
    ~Graph.node_laplacian
    ~Graph.node_neighborhood_centroid
    ~Graph.transform
    ~Graph.transformed

Paths
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.shortest_path

Planarity
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.count_crossings
    ~Graph.embed_in_plane
    ~Graph.find_crossings
    ~Graph.find_cycles
    ~Graph.is_crossed
    ~Graph.is_planar
    ~Graph.is_planar_embedding
    ~Graph.is_xy

Matrices
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.adjacency_matrix
    ~Graph.connectivity_matrix
    ~Graph.degree_matrix
    ~Graph.laplacian_matrix

Mappings
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.gkey_node
    ~Graph.node_gkey
    ~Graph.node_index
    ~Graph.edge_index
    ~Graph.index_node
    ~Graph.index_edge

Utilities
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Graph.summary
    ~Graph.copy
    ~Graph.clear
