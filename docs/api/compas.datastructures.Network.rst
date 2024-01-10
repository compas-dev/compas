******************************************************************************
Network
******************************************************************************

.. currentmodule:: compas.datastructures

.. autoclass:: Network

Methods
=======

Constructors
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.from_edges
    ~Network.from_json
    ~Network.from_lines
    ~Network.from_networkx
    ~Network.from_nodes_and_edges
    ~Network.from_obj
    ~Network.from_pointcloud

Conversions
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.to_json
    ~Network.to_lines
    ~Network.to_networkx
    ~Network.to_obj
    ~Network.to_points

Builders and Modifiers
----------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.add_edge
    ~Network.add_node
    ~Network.delete_edge
    ~Network.delete_node
    ~Network.join_edges
    ~Network.split_edge

Accessors
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.edge_sample
    ~Network.edges
    ~Network.edges_where
    ~Network.edges_where_predicate
    ~Network.node_sample
    ~Network.nodes
    ~Network.nodes_where
    ~Network.nodes_where_predicate

Attributes
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.edge_attribute
    ~Network.edge_attributes
    ~Network.edges_attribute
    ~Network.edges_attributes
    ~Network.node_attribute
    ~Network.node_attributes
    ~Network.nodes_attribute
    ~Network.nodes_attributes
    ~Network.update_default_edge_attributes
    ~Network.update_default_node_attributes
    ~Network.unset_edge_attribute
    ~Network.unset_node_attribute

Topology
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.complement
    ~Network.connected_nodes
    ~Network.connected_edges
    ~Network.degree
    ~Network.degree_out
    ~Network.degree_in
    ~Network.exploded
    ~Network.has_edge
    ~Network.has_node
    ~Network.is_leaf
    ~Network.is_node_connected
    ~Network.neighborhood
    ~Network.neighbors
    ~Network.neighbors_in
    ~Network.neighbors_out
    ~Network.node_edges
    ~Network.number_of_edges
    ~Network.number_of_nodes

Geometry
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.edge_coordinates
    ~Network.edge_direction
    ~Network.edge_end
    ~Network.edge_length
    ~Network.edge_line
    ~Network.edge_midpoint
    ~Network.edge_point
    ~Network.edge_start
    ~Network.edge_vector
    ~Network.node_coordinates
    ~Network.node_point
    ~Network.node_laplacian
    ~Network.node_neighborhood_centroid
    ~Network.transform
    ~Network.transformed

Paths
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.shortest_path

Planarity
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.count_crossings
    ~Network.embed_in_plane
    ~Network.find_crossings
    ~Network.find_cycles
    ~Network.is_crossed
    ~Network.is_planar
    ~Network.is_planar_embedding
    ~Network.is_xy

Matrices
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.adjacency_matrix
    ~Network.connectivity_matrix
    ~Network.degree_matrix
    ~Network.laplacian_matrix

Mappings
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.gkey_node
    ~Network.node_gkey
    ~Network.node_index
    ~Network.edge_index
    ~Network.index_node
    ~Network.index_edge

Utilities
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~Network.summary
    ~Network.copy
    ~Network.clear
