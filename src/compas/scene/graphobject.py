from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import transform_points

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject


class GraphObject(SceneObject):
    """Scene object for drawing graph data structures.

    Parameters
    ----------
    graph : :class:`compas.datastructures.Graph`
        A COMPAS graph.

    Attributes
    ----------
    graph : :class:`compas.datastructures.Graph`
        The COMPAS graph associated with the scene object.
    node_xyz : dict[hashable, list[float]]
        Mapping between nodes and their view coordinates.
        The default view coordinates are the actual coordinates of the nodes of the graph.
    nodecolor : :class:`compas.colors.ColorDict`
        Mapping between nodes and RGB color values.
    edgecolor : :class:`compas.colors.ColorDict`
        Mapping between edges and colors.
    nodesize : float
        The size of the nodes. Default is ``1.0``.
    edgewidth : float
        The width of the edges. Default is ``1.0``.
    show_nodes : Union[bool, sequence[float]]
        Flag for showing or hiding the nodes. Default is ``True``.
    show_edges : Union[bool, sequence[tuple[hashable, hashable]]]
        Flag for showing or hiding the edges. Default is ``True``.

    See Also
    --------
    :class:`compas.scene.MeshObject`
    :class:`compas.scene.VolMeshObject`

    """

    nodecolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()

    def __init__(self, graph, **kwargs):
        super(GraphObject, self).__init__(item=graph, **kwargs)
        self._graph = None
        self._node_xyz = None
        self.graph = graph
        self.nodecolor = kwargs.get("nodecolor", self.color)
        self.edgecolor = kwargs.get("edgecolor", self.color)
        self.nodesize = kwargs.get("nodesize", 1.0)
        self.edgewidth = kwargs.get("edgewidth", 1.0)
        self.show_nodes = kwargs.get("show_nodes", True)
        self.show_edges = kwargs.get("show_edges", True)

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        self._graph = graph
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
            points = self.graph.nodes_attributes("xyz")  # type: ignore
            points = transform_points(points, self.worldtransformation)
            self._node_xyz = dict(zip(self.graph.nodes(), points))  # type: ignore
        return self._node_xyz

    @node_xyz.setter
    def node_xyz(self, node_xyz):
        self._node_xyz = node_xyz

    def draw_nodes(self, nodes=None, color=None, text=None):
        """Draw the nodes of the graph.

        Parameters
        ----------
        nodes : list[int], optional
            The nodes to include in the drawing.
            Default is all nodes.
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[int, tuple[float, float, float] | :class:`compas.colors.Color`], optional
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

    def draw_edges(self, edges=None, color=None, text=None):
        """Draw the edges of the graph.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            The edges to include in the drawing.
            Default is all edges.
        color : tuple[float, float, float] | :class:`compas.colors.Color` | dict[tuple[int, int], tuple[float, float, float] | :class:`compas.colors.Color`], optional
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

    def draw(self):
        """Draw the network."""
        raise NotImplementedError

    def clear_nodes(self):
        """Clear the nodes of the graph.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear_edges(self):
        """Clear the edges of the graph.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear(self):
        """Clear the nodes and the edges of the graph.

        Returns
        -------
        None

        """
        self.clear_nodes()
        self.clear_edges()
