import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
from compas.datastructures import Tree
from compas.datastructures import TreeNode

from .context import after_draw
from .context import before_draw
from .context import clear
from .context import detect_current_context
from .sceneobject import SceneObject


class Scene(Tree):
    """A scene is a container for hierarchical scene objects which are to be visualised in a given context.

    Parameters
    ----------
    name : str, optional
        The name of the scene.
    context : str, optional
        The context in which the scene is visualised. Will be automatically detected if not specified.

    Attributes
    ----------
    tree : :class:`compas.scene.SceneTree`
        The underlying tree data structure of the scene.
    objects : list[:class:`compas.scene.SceneObject`]
        All scene objects in the scene.

    Examples
    --------
    >>> from compas.scene import Scene
    >>> from compas.geometry import Box
    >>> scene = Scene()
    >>> box = Box.from_width_height_depth(1, 1, 1)
    >>> boxobj = scene.add(box)
    >>> scene.draw()  # doctest: +SKIP

    """

    @property
    def __data__(self):
        # type: () -> dict
        items = {str(object.item.guid): object.item for object in self.objects}
        return {
            "name": self.name,
            "root": self.root.__data__,  # type: ignore
            "items": list(items.values()),
        }

    @classmethod
    def __from_data__(cls, data):
        # type: (dict) -> Scene
        scene = cls(data["name"])
        items = {str(item.guid): item for item in data["items"]}

        def add(node, parent, items):
            for child_node in node["children"]:
                guid = child_node["item"]
                settings = child_node["settings"]
                sceneobject = parent.add(items[guid], **settings)
                add(child_node, sceneobject, items)

        add(data["root"], scene, items)

        return scene

    def __init__(self, name="Scene", context=None):
        # type: (str | "Scene", str | None) -> None
        super(Scene, self).__init__(name=name)
        super(Scene, self).add(TreeNode(name="ROOT"))
        self.context = context or detect_current_context()

    @property
    def objects(self):
        # type: () -> list[SceneObject]
        # this is flagged by the type checker
        # because the tree returns nodes of type TreeNode
        return [node for node in self.nodes if not node.is_root]  # type: ignore

    def add(self, item, parent=None, **kwargs):
        # type: (compas.geometry.Geometry | compas.datastructures.Datastructure, SceneObject | TreeNode | None, dict) -> SceneObject
        """Add an item to the scene.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            The item to add.
        parent : :class:`compas.data.Data`, optional
            The parent item.
        **kwargs : dict
            Additional keyword arguments to create the scene object for the item.

        Returns
        -------
        :class:`compas.scene.SceneObject`
            The scene object associated with the item.
        """

        parent = parent or self.root

        if isinstance(item, SceneObject):
            sceneobject = item
        else:
            if "context" in kwargs:
                if kwargs["context"] != self.context:
                    raise Exception("Object context should be the same as scene context: {} != {}".format(kwargs["context"], self.context))
                del kwargs["context"]  # otherwist the SceneObject receives "context" twice, which results in an error
            sceneobject = SceneObject(item, context=self.context, **kwargs)  # type: ignore
        super(Scene, self).add(sceneobject, parent=parent)
        return sceneobject

    def clear(self):
        # type: () -> None
        """Clear the current context of the scene."""
        clear()

    def clear_objects(self):
        # type: () -> None
        """Clear all objects inside the scene."""
        guids = []
        for sceneobject in self.objects:
            guids += sceneobject.guids
            sceneobject._guids = None
        clear(guids=guids)

    def draw(self):
        """Draw the scene."""

        before_draw()

        if not self.context:
            raise ValueError("No context detected.")

        self.clear_objects()

        drawn_objects = []
        for sceneobject in self.objects:
            if sceneobject.show:
                drawn_objects += sceneobject.draw()

        after_draw(drawn_objects)

        return drawn_objects
