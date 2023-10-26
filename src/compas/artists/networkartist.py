from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.colors import Color
from compas.geometry import transform_points
from .artist import Artist
from .descriptors.colordict import ColorDictAttribute


class NetworkArtist(Artist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A COMPAS network.

    Attributes
    ----------
    network : :class:`~compas.datastructures.Network`
        The COMPAS network associated with the artist.
    node_xyz : dict[hashable, list[float]]
        Mapping between nodes and their view coordinates.
        The default view coordinates are the actual coordinates of the nodes of the network.
    node_color : :class:`~compas.colors.ColorDict`
        Mapping between nodes and RGB color values.
    edge_color : :class:`~compas.colors.ColorDict`
        Mapping between edges and colors.

    See Also
    --------
    :class:`compas.artists.MeshArtist`
    :class:`compas.artists.VolMeshArtist`

    """

    node_color = ColorDictAttribute(default=Color.white())
    edge_color = ColorDictAttribute(default=Color.black())

    def __init__(self, network, **kwargs):
        super(NetworkArtist, self).__init__(**kwargs)
        self._network = None
        self._node_xyz = None
        self.network = network

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network
        self._transformation = None
        self._node_xyz = None

    @property
    def transformation(self):
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._node_xyz = None
        self._transformation = transformation

    @property
    def node_xyz(self):
        if self._node_xyz is None:
            points = self.network.nodes_attributes("xyz")  # type: ignore
            if self.transformation:
                points = transform_points(points, self.transformation)
            self._node_xyz = dict(zip(self.network.nodes(), points))  # type: ignore
        return self._node_xyz

    @node_xyz.setter
    def node_xyz(self, node_xyz):
        self._node_xyz = node_xyz

    @abstractmethod
    def draw_nodes(self, nodes=None, color=None, text=None):
        """Draw the nodes of the network.

        Parameters
        ----------
        nodes : list[int], optional
            The nodes to include in the drawing.
            Default is all nodes.
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`~compas.colors.Color`], optional
            The color of the nodes,
            as either a single color to be applied to all nodes,
            or a color dict, mapping specific nodes to specific colors.
        text : dict[int, str], optional
            The text labels for the nodes
            as a text dict, mapping specific nodes to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the nodes in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_edges(self, edges=None, color=None, text=None):
        """Draw the edges of the network.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            The edges to include in the drawing.
            Default is all edges.
        color : tuple[float, float, float] | :class:`~compas.colors.Color` | dict[tuple[int, int], tuple[float, float, float] | :class:`~compas.colors.Color`], optional
            The color of the edges,
            as either a single color to be applied to all edges,
            or a color dict, mapping specific edges to specific colors.
        text : dict[tuple[int, int]], optional
            The text labels for the edges
            as a text dict, mapping specific edges to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    def clear_nodes(self):
        """Clear the nodes of the network.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_edges(self):
        """Clear the edges of the network.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear(self):
        """Clear the nodes and the edges of the network.

        Returns
        -------
        None

        """
        self.clear_nodes()
        self.clear_edges()
