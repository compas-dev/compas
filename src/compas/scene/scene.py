import compas.data  # noqa: F401
import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
from compas.datastructures import Tree
from compas.datastructures import TreeNode

from .context import after_draw
from .context import before_draw
from .context import clear
from .context import detect_current_context
from .group import Group
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
        items = {str(object.item.guid): object.item for object in self.objects if object.item is not None}
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
            for child_node in node.get("children", []):
                settings = child_node["settings"]
                if "item" in child_node:
                    guid = child_node["item"]
                    sceneobject = parent.add(items[guid], **settings)
                else:
                    sceneobject = parent.add(Group(**settings))
                add(child_node, sceneobject, items)

        add(data["root"], scene, items)

        return scene

    def __init__(self, name="Scene", context=None):
        # type: (str, str | None) -> None
        super(Scene, self).__init__(name=name)
        super(Scene, self).add(TreeNode(name="ROOT"))
        self.context = context or detect_current_context()

    @property
    def objects(self):
        # type: () -> list[SceneObject]
        return [node for node in self.nodes if not node.is_root]  # type: ignore

    @property
    def context_objects(self):
        # type: () -> list
        guids = []
        for obj in self.objects:
            guids += obj.guids
        return guids

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
            sceneobject = SceneObject(item=item, context=self.context, **kwargs)  # type: ignore
        super(Scene, self).add(sceneobject, parent=parent)
        return sceneobject

    def clear_context(self, guids=None):
        # type: (list | None) -> None
        """Clear the visualisation context.

        Parameters
        ----------
        guids : list, optional
            The identifiers of the objects in the visualisation context.

        Returns
        -------
        None

        Notes
        -----
        If `guids=None`, this will clear all objects from the visualisation context.
        For example, when used in Rhino, it will remove everything from the Rhino model.
        This is equivalent to `compas_rhino.clear()`.

        If `guids` is a list, only those objects in the list will be removed.

        The method is used by `Scene.clear` to remove all objects previously drawn by the scene,
        without removing other model objects.

        """
        clear(guids)

    def clear(self, clear_scene=True, clear_context=True):
        # type: (bool, bool) -> None
        """Clear the scene.

        Parameters
        ----------
        clear_scene : bool, optional
            If True, all scene objects will be removed from the scene tree.
        clear_context : bool, optional
            If True, all objects drawn by the scene in the visualisation context will be removed.

        Returns
        -------
        None

        Notes
        -----
        To redraw the scene, without modifying any of the other objects in the visualisation context:

        >>> scene.clear(clear_scene=False, clear_context=True)  # doctest: +SKIP
        >>> scene.draw()  # doctest: +SKIP

        """
        guids = []

        for sceneobject in self.objects:
            guids += sceneobject.guids
            sceneobject._guids = None

            if clear_scene:
                self.remove(sceneobject)

        if clear_context:
            self.clear_context(guids)

    def draw(self):
        """Draw the scene.

        This will just draw all scene objects in the scene tree,
        without making any modifications to the visualisation context.
        For example, it will not remove any of the previously drawn objects.

        """

        if not self.context:
            raise ValueError("No context detected.")

        before_draw()

        drawn_objects = []
        for sceneobject in self.objects:
            if sceneobject.show:
                drawn_objects += sceneobject.draw()

        after_draw(drawn_objects)

        return drawn_objects

    def redraw(self):
        """Redraw the scene.

        This removes all previously drawn objects from the visualisation context,
        before drawing all scene objects in the scene tree.

        """
        self.clear(clear_scene=False, clear_context=True)
        self.draw()

    def find_by_name(self, name):
        # type: (str) -> SceneObject
        """Find the first scene object with the given name.

        Parameters
        ----------
        name : str
            Name of the object.

        Returns
        -------
        :class:`SceneObject`

        """
        return self.get_node_by_name(name=name)

    def find_by_itemtype(self, itemtype):
        # type: (...) -> SceneObject | None
        """Find the first scene object with a data item of the given type.

        Parameters
        ----------
        itemtype : :class:`compas.data.Data`
            The type of the data item associated with the scene object.

        Returns
        -------
        :class:`SceneObject` or None

        """
        for obj in self.objects:
            if isinstance(obj.item, itemtype):
                return obj

    def find_all_by_itemtype(self, itemtype):
        # type: (...) -> list[SceneObject]
        """Find all scene objects with a data item of the given type.

        Parameters
        ----------
        itemtype : :class:`compas.data.Data`
            The type of the data item associated with the scene object.

        Returns
        -------
        list[:class:`SceneObject`]

        """
        sceneobjects = []
        for obj in self.objects:
            if isinstance(obj.item, itemtype):
                sceneobjects.append(obj)
        return sceneobjects
