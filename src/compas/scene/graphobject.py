from collections.abc import Hashable
from collections.abc import Mapping
from typing import Any
from typing import cast

from compas.colors import Color
from compas.colors.color import ColorInput
from compas.datastructures import Graph
from compas.geometry import transform_points

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject


class GraphObject(SceneObject):
    """Scene object for drawing graph data structures.

    See Also
    --------
    [`MeshObject`][compas.scene.MeshObject]
    [`VolMeshObject`][compas.scene.VolMeshObject]

    """

    nodecolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(
        self,
        show_nodes: bool | list[Hashable] = True,
        show_edges: bool | list[tuple[Hashable, Hashable]] = True,
        nodecolor: Mapping[Any, ColorInput] | Color | None = None,
        edgecolor: Mapping[Any, ColorInput] | Color | None = None,
        nodesize: float = 1.0,
        edgewidth: float = 1.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._node_xyz: dict[Hashable, list[float]] | None = None
        self._node_xyz_revision: tuple[int, ...] | None = None
        self.show_nodes = show_nodes
        self.show_edges = show_edges
        self.nodecolor = nodecolor or self.color
        self.edgecolor = edgecolor or self.color
        self.nodesize = nodesize
        self.edgewidth = edgewidth

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def settings(self) -> dict[str, object]:
        """The settings required to reconstruct the graph scene object."""
        settings = super().settings
        settings["show_nodes"] = self.show_nodes
        settings["show_edges"] = self.show_edges
        settings["nodecolor"] = self.nodecolor
        settings["edgecolor"] = self.edgecolor
        settings["nodesize"] = self.nodesize
        settings["edgewidth"] = self.edgewidth
        return settings

    @property
    def graph(self) -> Graph:
        """The graph represented by this scene object.

        Setting the graph clears the local transformation and cached node
        coordinates.

        """
        return cast(Graph, self.item)

    @graph.setter
    def graph(self, graph: Graph) -> None:
        self._item = graph
        self._transformation = None
        self._node_xyz = None
        self._node_xyz_revision = None

    @property
    def node_xyz(self) -> dict[Hashable, list[float]]:
        """The node coordinates in the scene object's world coordinate system.

        Notes
        -----
        Coordinates computed from the graph are cached until the local or an
        ancestor transformation changes. Explicitly assigned coordinates are
        used as-is until the local transformation or graph changes.

        """
        revision = self._worldtransformation_revision()
        if self._node_xyz is None or (self._node_xyz_revision is not None and self._node_xyz_revision != revision):
            points = self.graph.nodes_attributes("xyz")
            points = transform_points(points, self.worldtransformation)
            self._node_xyz = dict(zip(self.graph.nodes(), points))
            self._node_xyz_revision = revision
        return self._node_xyz

    @node_xyz.setter
    def node_xyz(self, node_xyz: dict[Hashable, list[float]]) -> None:
        self._node_xyz = node_xyz
        self._node_xyz_revision = None

    # ==========================================================================
    # Methods
    # ==========================================================================

    def draw_nodes(self) -> list[object]:
        """Draw the nodes of the graph.

        Nodes are drawn based on the values of

        * `self.show_nodes`
        * `self.nodecolor`
        * `self.nodesize`

        Returns
        -------
        list[object]
            The identifiers of the objects representing the nodes in the visualization context.

        """
        raise NotImplementedError

    def draw_edges(self) -> list[object]:
        """Draw the edges of the graph.

        Edges are drawn based on the values of

        * `self.show_edges`
        * `self.edgecolor`
        * `self.edgewidth`

        Returns
        -------
        list[object]
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    def clear_nodes(self) -> None:
        """Clear the nodes of the graph."""
        raise NotImplementedError

    def clear_edges(self) -> None:
        """Clear the edges of the graph."""
        raise NotImplementedError

    def clear(self) -> None:
        """Clear the nodes and edges of the graph."""
        self.clear_nodes()
        self.clear_edges()

    # ==========================================================================
    # Private helpers
    # ==========================================================================

    def _invalidate_transformation_cache(self) -> None:
        self._node_xyz = None
        self._node_xyz_revision = None
