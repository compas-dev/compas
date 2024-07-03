from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.colors  # noqa: F401
import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
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
    show_nodes : Union[bool, sequence[hashable]]
        Flag for showing or hiding the nodes. Default is ``True``.
    show_edges : Union[bool, sequence[tuple[hashable, hashable]]]
        Flag for showing or hiding the edges. Default is ``True``.
    nodecolor : :class:`compas.colors.ColorDict`
        Mapping between nodes and RGB color values.
    edgecolor : :class:`compas.colors.ColorDict`
        Mapping between edges and colors.
    nodesize : float
        The size of the nodes. Default is ``1.0``.
    edgewidth : float
        The width of the edges. Default is ``1.0``.

    See Also
    --------
    :class:`compas.scene.MeshObject`
    :class:`compas.scene.VolMeshObject`

    """

    nodecolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()

    def __init__(
        self,
        show_nodes=True,  # type: bool | list
        show_edges=True,  # type: bool | list
        nodecolor=None,  # type: dict | compas.colors.Color | None
        edgecolor=None,  # type: dict | compas.colors.Color | None
        nodesize=1.0,  # type: float
        edgewidth=1.0,  # type: float
        **kwargs  # type: dict
    ):  # fmt: skip
        # type: (...) -> None
        super(GraphObject, self).__init__(**kwargs)  # type: ignore
        self._node_xyz = None
        self.show_nodes = show_nodes
        self.show_edges = show_edges
        self.nodecolor = nodecolor or self.color
        self.edgecolor = edgecolor or self.color
        self.nodesize = nodesize
        self.edgewidth = edgewidth

    @property
    def settings(self):
        # type: () -> dict
        settings = super(GraphObject, self).settings
        settings["show_nodes"] = self.show_nodes
        settings["show_edges"] = self.show_edges
        settings["nodecolor"] = self.nodecolor
        settings["edgecolor"] = self.edgecolor
        settings["nodesize"] = self.nodesize
        settings["edgewidth"] = self.edgewidth
        return settings

    @property
    def graph(self):
        # type: () -> compas.datastructures.Graph
        return self.item  # type: ignore

    @graph.setter
    def graph(self, graph):
        # type: (compas.datastructures.Graph) -> None
        self._item = graph
        self._transformation = None
        self._node_xyz = None

    @property
    def transformation(self):
        # type: () -> compas.geometry.Transformation | None
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        # type: (compas.geometry.Transformation) -> None
        self._node_xyz = None
        self._transformation = transformation

    @property
    def node_xyz(self):
        # type: () -> dict[int | str, list[float]]
        if self.graph:
            if self._node_xyz is None:
                points = self.graph.nodes_attributes("xyz")
                points = transform_points(points, self.worldtransformation)
                self._node_xyz = dict(zip(self.graph.nodes(), points))
        return self._node_xyz  # type: ignore

    @node_xyz.setter
    def node_xyz(self, node_xyz):
        # type: (dict[int | str, list[float]]) -> None
        self._node_xyz = node_xyz

    def draw_nodes(self):
        """Draw the nodes of the graph.

        Nodes are drawn based on the values of

        * `self.show_nodes`
        * `self.nodecolor`
        * `self.nodesize`

        Returns
        -------
        list
            The identifiers of the objects representing the nodes in the visualization context.

        """
        raise NotImplementedError

    def draw_edges(self):
        """Draw the edges of the graph.

        Edges are drawn based on the values of

        * `self.show_edges`
        * `self.edgecolor`
        * `self.edgewidth`

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
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
