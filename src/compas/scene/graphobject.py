from collections.abc import Hashable
from collections.abc import Mapping
from typing import Any
from typing import cast

from compas.colors import Color
from compas.colors.color import ColorInput
from compas.datastructures import Graph
from compas.geometry import transform_points
from compas.typing import RealInput

from .descriptors.colordict import ColorDictAttribute
from .sceneobject import SceneObject
from .sceneobject import SceneStateField


class GraphObject(SceneObject):
    """Scene object for drawing graph data structures.

    See Also
    --------
    [`MeshObject`][compas.scene.MeshObject]
    [`VolMeshObject`][compas.scene.VolMeshObject]

    """

    nodecolor = ColorDictAttribute()
    edgecolor = ColorDictAttribute()
    __scene_state_namespace__ = "compas.scene.GraphObject"
    __scene_state_fields__ = (
        SceneStateField("show_nodes", (bool, list), default=True, required=False, editable=True),
        SceneStateField("show_edges", (bool, list), default=True, required=False, editable=True),
        SceneStateField("nodecolor", required=False, editable=True),
        SceneStateField("edgecolor", required=False, editable=True),
        SceneStateField("edgewidth", (int, float), default=1.0, required=False, editable=True),
        SceneStateField("nodesize", (int, float), default=1.0, required=False, editable=True),
    )

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
        self._node_xyz: dict[Hashable, list[RealInput]] | None = None
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
    def graph(self) -> Graph:
        """The graph represented by this scene object.

        Setting the graph clears the local transformation and cached node
        coordinates.

        """
        return cast(Graph, self.item)

    @graph.setter
    def graph(self, graph: Graph) -> None:
        if self.scene is None:
            self._item_guid = graph.guid
            self._item = graph
        else:
            self.scene.replace_item(self, graph)
        self.transformation = None
        self._node_xyz = None
        self._node_xyz_revision = None

    @property
    def node_xyz(self) -> dict[Hashable, list[RealInput]]:
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
    def node_xyz(self, node_xyz: dict[Hashable, list[RealInput]]) -> None:
        self._node_xyz = node_xyz
        self._node_xyz_revision = None

    # ==========================================================================
    # Private helpers
    # ==========================================================================

    def _invalidate_transformation_cache(self) -> None:
        self._node_xyz = None
        self._node_xyz_revision = None
