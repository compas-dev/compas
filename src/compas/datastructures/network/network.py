from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

if compas.PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping

from compas.tolerance import TOL
from compas.files import OBJ
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import centroid_points
from compas.geometry import subtract_vectors
from compas.geometry import distance_point_point
from compas.geometry import midpoint_line
from compas.geometry import normalize_vector
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import transform_points
from compas.topology import astar_shortest_path

from compas.datastructures import Graph

from .operations.split import network_split_edge
from .operations.join import network_join_edges

from .planarity import network_is_crossed
from .planarity import network_is_planar
from .planarity import network_is_planar_embedding
from .planarity import network_is_xy
from .planarity import network_count_crossings
from .planarity import network_find_crossings
from .planarity import network_embed_in_plane
from .smoothing import network_smooth_centroid
from .duality import network_find_cycles


class Network(Graph):
    """Geometric implementation of an edge graph.

    Parameters
    ----------
    default_node_attributes: dict, optional
        Default values for node attributes.
    default_edge_attributes: dict, optional
        Default values for edge attributes.
    **kwargs : dict, optional
        Additional attributes to add to the network.

    """

    split_edge = network_split_edge
    join_edges = network_join_edges
    smooth = network_smooth_centroid

    is_crossed = network_is_crossed
    is_planar = network_is_planar
    is_planar_embedding = network_is_planar_embedding
    is_xy = network_is_xy
    count_crossings = network_count_crossings
    find_crossings = network_find_crossings
    embed_in_plane = network_embed_in_plane

    find_cycles = network_find_cycles

    def __init__(self, default_node_attributes=None, default_edge_attributes=None, **kwargs):
        _default_node_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        _default_edge_attributes = {}
        if default_node_attributes:
            _default_node_attributes.update(default_node_attributes)
        if default_edge_attributes:
            _default_edge_attributes.update(default_edge_attributes)
        super(Network, self).__init__(
            default_node_attributes=_default_node_attributes, default_edge_attributes=_default_edge_attributes, **kwargs
        )

    def __str__(self):
        tpl = "<Network with {} nodes, {} edges>"
        return tpl.format(self.number_of_nodes(), self.number_of_edges())

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, precision=None):
        """Construct a network from the data contained in an OBJ file.

        Parameters
        ----------
        filepath : path string | file-like object | URL string
            A path, a file-like object or a URL pointing to a file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        :class:`compas.datastructures.Network`
            A network object.

        See Also
        --------
        :meth:`to_obj`
        :meth:`from_lines`, :meth:`from_nodes_and_edges`, :meth:`from_pointcloud`
        :class:`compas.files.OBJ`

        """
        network = cls()
        obj = OBJ(filepath, precision)
        obj.read()
        nodes = obj.vertices
        edges = obj.lines
        for i, (x, y, z) in enumerate(nodes):  # type: ignore
            network.add_node(i, x=x, y=y, z=z)
        for edge in edges:  # type: ignore
            network.add_edge(*edge)
        return network

    @classmethod
    def from_lines(cls, lines, precision=None):
        """Construct a network from a set of lines represented by their start and end point coordinates.

        Parameters
        ----------
        lines : list[tuple[list[float, list[float]]]]
            A list of pairs of point coordinates.
        precision : int, optional
            Precision for converting numbers to strings.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        :class:`compas.datastructures.Network`
            A network object.

        See Also
        --------
        :meth:`to_lines`
        :meth:`from_obj`, :meth:`from_nodes_and_edges`, :meth:`from_pointcloud`

        """
        network = cls()
        edges = []
        node = {}
        for line in lines:
            sp = line[0]
            ep = line[1]
            a = TOL.geometric_key(sp, precision)
            b = TOL.geometric_key(ep, precision)
            node[a] = sp
            node[b] = ep
            edges.append((a, b))
        key_index = dict((k, i) for i, k in enumerate(iter(node)))
        for key, xyz in iter(node.items()):
            i = key_index[key]
            network.add_node(i, x=xyz[0], y=xyz[1], z=xyz[2])
        for u, v in edges:
            i = key_index[u]
            j = key_index[v]
            network.add_edge(i, j)
        return network

    @classmethod
    def from_nodes_and_edges(cls, nodes, edges):
        """Construct a network from nodes and edges.

        Parameters
        ----------
        nodes : list[list[float]] | dict[hashable, list[float]]
            A list of node coordinates or a dictionary of keys pointing to node coordinates to specify keys.
        edges : list[tuple[hashable, hshable]]

        Returns
        -------
        :class:`compas.datastructures.Network`
            A network object.

        See Also
        --------
        :meth:`to_nodes_and_edges`
        :meth:`from_obj`, :meth:`from_lines`, :meth:`from_pointcloud`

        """
        network = cls()

        if isinstance(nodes, Mapping):
            for key, (x, y, z) in nodes.items():
                network.add_node(key, x=x, y=y, z=z)
        else:
            for i, (x, y, z) in enumerate(nodes):
                network.add_node(i, x=x, y=y, z=z)

        for u, v in edges:
            network.add_edge(u, v)

        return network

    @classmethod
    def from_pointcloud(cls, cloud, degree=3):
        """Construct a network from random connections between the points of a pointcloud.

        Parameters
        ----------
        cloud : :class:`compas.geometry.Pointcloud`
            A pointcloud object.
        degree : int, optional
            The number of connections per node.

        Returns
        -------
        :class:`compas.datastructures.Network`
            A network object.

        See Also
        --------
        :meth:`to_points`
        :meth:`from_obj`, :meth:`from_lines`, :meth:`from_nodes_and_edges`

        """
        network = cls()
        for x, y, z in cloud:
            network.add_node(x=x, y=y, z=z)
        for u in network.nodes():
            for v in network.node_sample(size=degree):
                network.add_edge(u, v)
        return network

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self):
        """Write the network to an OBJ file.

        Parameters
        ----------
        filepath : path string | file-like object
            A path or a file-like object pointing to a file.

        Returns
        -------
        None

        See Also
        --------
        :meth:`from_obj`
        :meth:`to_lines`, :meth:`to_nodes_and_edges`, :meth:`to_points`

        """
        raise NotImplementedError

    def to_points(self):
        """Return the coordinates of the network.

        Returns
        -------
        list[list[float]]
            A list with the coordinates of the vertices of the network.

        See Also
        --------
        :meth:`from_pointcloud`
        :meth:`to_lines`, :meth:`to_nodes_and_edges`, :meth:`to_obj`

        """
        return [self.node_coordinates(key) for key in self.nodes()]

    def to_lines(self):
        """Return the lines of the network as pairs of start and end point coordinates.

        Returns
        -------
        list[tuple[list[float], list[float]]]
            A list of lines each defined by a pair of point coordinates.

        See Also
        --------
        :meth:`from_lines`
        :meth:`to_nodes_and_edges`, :meth:`to_obj`, :meth:`to_points`

        """
        return [self.edge_coordinates(edge) for edge in self.edges()]

    def to_nodes_and_edges(self):
        """Return the nodes and edges of a network.

        Returns
        -------
        list[list[float]]
            A list of nodes, represented by their XYZ coordinates.
        list[tuple[hashable, hashable]]
            A list of edges, with each edge represented by a pair of indices in the node list.

        See Also
        --------
        :meth:`from_nodes_and_edges`
        :meth:`to_lines`, :meth:`to_obj`, :meth:`to_points`

        """
        key_index = dict((key, index) for index, key in enumerate(self.nodes()))
        nodes = [self.node_coordinates(key) for key in self.nodes()]
        edges = [(key_index[u], key_index[v]) for u, v in self.edges()]
        return nodes, edges

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def node_gkey(self, precision=None):
        """Returns a dictionary that maps node identifiers to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision : int, optional
            Precision for converting numbers to strings.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        dict[hashable, str]
            A dictionary of (node, geometric key) pairs.

        See Also
        --------
        :meth:`gkey_node`
        :meth:`compas.Tolerance.geometric_key`

        """
        gkey = TOL.geometric_key
        xyz = self.node_coordinates
        return {key: gkey(xyz(key), precision) for key in self.nodes()}

    def gkey_node(self, precision=None):
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the identifiers of the corresponding nodes.

        Parameters
        ----------
        precision : int, optional
            Precision for converting numbers to strings.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        dict[str, hashable]
            A dictionary of (geometric key, node) pairs.

        See Also
        --------
        :meth:`node_gkey`
        :meth:`compas.Tolerance.geometric_key`

        """
        gkey = TOL.geometric_key
        xyz = self.node_coordinates
        return {gkey(xyz(key), precision): key for key in self.nodes()}

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def shortest_path(self, u, v):
        """Find the shortest path between two nodes using the A* algorithm.

        Parameters
        ----------
        u : hashable
            The identifier of the start node.
        v : hashable
            The identifier of the end node.

        Returns
        -------
        list[hashable] | None
            The path from root to goal, or None, if no path exists between the vertices.

        See Also
        --------
        :meth:`compas.topology.astar_shortest_path`

        """
        return astar_shortest_path(self.adjacency, u, v)

    # --------------------------------------------------------------------------
    # node attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # edge attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # node topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # node geometry
    # --------------------------------------------------------------------------

    def node_coordinates(self, key, axes="xyz"):
        """Return the coordinates of a node.

        Parameters
        ----------
        key : hashable
            The identifier of the node.
        axes : str, optional
            The components of the node coordinates to return.

        Returns
        -------
        list[float]
            The coordinates of the node.

        See Also
        --------
        :meth:`node_point`, :meth:`node_laplacian`, :meth:`node_neighborhood_centroid`

        """
        return [self.node[key][axis] for axis in axes]

    def node_point(self, node):
        """Return the point of a node.

        Parameters
        ----------
        node : hashable
            The identifier of the node.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point of the node.

        See Also
        --------
        :meth:`node_coordinates`, :meth:`node_laplacian`, :meth:`node_neighborhood_centroid`

        """
        return Point(*self.node_coordinates(node))

    def node_laplacian(self, key):
        """Return the vector from the node to the centroid of its 1-ring neighborhood.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The laplacian vector.

        See Also
        --------
        :meth:`node_coordinates`, :meth:`node_point`, :meth:`node_neighborhood_centroid`

        """
        c = centroid_points([self.node_coordinates(nbr) for nbr in self.neighbors(key)])
        p = self.node_coordinates(key)
        return Vector(*subtract_vectors(c, p))

    def node_neighborhood_centroid(self, key):
        """Return the computed centroid of the neighboring nodes.

        Parameters
        ----------
        key : hashable
            The identifier of the node.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the centroid.

        See Also
        --------
        :meth:`node_coordinates`, :meth:`node_point`, :meth:`node_laplacian`

        """
        return Point(*centroid_points([self.node_coordinates(nbr) for nbr in self.neighbors(key)]))

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, edge, axes="xyz"):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.
        axes : str, optional
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple[list[float], list[float]]
            The coordinates of the start point.
            The coordinates of the end point.

        See Also
        --------
        :meth:`edge_point`, :meth:`edge_start`, :meth:`edge_end`, :meth:`edge_midpoint`

        """
        u, v = edge
        return self.node_coordinates(u, axes=axes), self.node_coordinates(v, axes=axes)

    def edge_start(self, edge):
        """Return the start point of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Point`
            The start point of the edge.

        See Also
        --------
        :meth:`edge_point`, :meth:`edge_end`, :meth:`edge_midpoint`

        """
        return self.node_point(edge[0])

    def edge_end(self, edge):
        """Return the end point of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Point`
            The end point of the edge.

        See Also
        --------
        :meth:`edge_point`, :meth:`edge_start`, :meth:`edge_midpoint`

        """
        return self.node_point(edge[1])

    def edge_point(self, edge, t=0.5):
        """Return the point at a parametric location along an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.
        t : float, optional
            The location of the point on the edge.
            If the value of `t` is outside the range 0-1, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the specified location.

        See Also
        --------
        :meth:`edge_start`, :meth:`edge_end`, :meth:`edge_midpoint`

        """
        if t == 0.0:
            return self.edge_start(edge)
        if t == 1.0:
            return self.edge_end(edge)
        if t == 0.5:
            return self.edge_midpoint(edge)

        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return Point(*add_vectors(a, scale_vector(ab, t)))

    def edge_midpoint(self, edge):
        """Return the location of the midpoint of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Point`
            The midpoint of the edge.

        See Also
        --------
        :meth:`edge_start`, :meth:`edge_end`, :meth:`edge_point`

        """
        a, b = self.edge_coordinates(edge)
        return Point(*midpoint_line((a, b)))

    def edge_vector(self, edge):
        """Return the vector of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The vector from start to end.

        See Also
        --------
        :meth:`edge_direction`, :meth:`edge_line`, :meth:`edge_length`

        """
        a, b = self.edge_coordinates(edge)
        return Vector.from_start_end(a, b)

    def edge_direction(self, edge):
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The direction vector of the edge.

        See Also
        --------
        :meth:`edge_vector`, :meth:`edge_line`, :meth:`edge_length`

        """
        return Vector(*normalize_vector(self.edge_vector(edge)))

    def edge_line(self, edge):
        """Return the line of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Line`
            The line of the edge.

        See Also
        --------
        :meth:`edge_vector`, :meth:`edge_direction`, :meth:`edge_length`

        """
        return Line(*self.edge_coordinates(edge))

    def edge_length(self, edge):
        """Return the length of an edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        float
            The length of the edge.

        See Also
        --------
        :meth:`edge_vector`, :meth:`edge_direction`, :meth:`edge_line`

        """
        a, b = self.edge_coordinates(edge)
        return distance_point_point(a, b)

    # --------------------------------------------------------------------------
    # transformations
    # --------------------------------------------------------------------------

    def transform(self, transformation):
        """Transform all nodes of the network.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the nodes.

        Returns
        -------
        None

        """
        nodes = self.nodes_attributes("xyz")
        points = transform_points(nodes, transformation)
        for point, node in zip(points, self.nodes()):
            self.node_attributes(node, "xyz", point)
