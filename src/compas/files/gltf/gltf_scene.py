from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import Optional

from compas.files.gltf.gltf_children import GLTFChildren

if TYPE_CHECKING:
    from .gltf_document import GLTFDocument
    from .gltf_node import GLTFNode


class GLTFScene:
    """Object representing the COMPAS consumable part of a glTF scene.

    Attributes
    ----------
    name : str
        Name of the scene.
    children : GLTFChildren
        Validated list of keys referencing GLTFScene.context.nodes.
    extras : object
    extensions : object
    context : GLTFDocument
        GLTF context in which the scene exists.
    key : int
        Key of the scene within GLTFDocument.scenes.
    nodes : dict
        Dictionary of nodes in the given scene, without a specified root.
    positions_and_edges : tuple
        Tuple containing a dictionary of positions and a list of tuples representing edges.

    """

    def __init__(
        self,
        context: "GLTFDocument",
        children: Optional[Iterable[int]] = None,
        name: Optional[str] = None,
        extras: Any = None,
        extensions: Any = None,
    ) -> None:
        self.name = name
        self._children = GLTFChildren(context, children or [])
        self.extras = extras
        self.extensions = extensions

        self._key = None
        self.context = context
        self._set_key()

    def _set_key(self) -> None:
        key = len(self.context.scenes)
        while key in self.context.scenes:
            key += 1
        self.context.scenes[key] = self
        self._key = key

    @property
    def key(self) -> int:
        assert self._key is not None
        return self._key

    @property
    def children(self) -> GLTFChildren:
        return self._children

    @children.setter
    def children(self, value: Optional[Iterable[int]]) -> None:
        self._children = GLTFChildren(self.context, value or [])

    @property
    def nodes(self) -> dict[int, "GLTFNode"]:
        return self.context.get_nodes_from_scene(self)

    @property
    def positions_and_edges(self):
        return self.context.get_scene_positions_and_edges(self)

    def add_child(self, node_name: Optional[str] = None, node_extras: Any = None) -> "GLTFNode":
        """Create a node and add it as a scene root.

        Parameters
        ----------
        node_name
            Optional node name.
        node_extras
            Application-specific node data.

        Returns
        -------
        GLTFNode
            Created node.

        """
        return self.context.add_node_to_scene(self, node_name, node_extras)
