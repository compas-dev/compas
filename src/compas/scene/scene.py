from compas.data import Data
from compas.datastructures import Tree
from compas.datastructures import TreeNode

from .context import clear
from .context import redraw
from .context import detect_current_context
from .sceneobject import SceneObject


class SceneObjectNode(TreeNode):
    """A node representing a scene object in a scene tree. The SceneObjectNode should only be used internally by the SceneTree.

    Parameters
    ----------
    object : :class:`compas.scene.SceneObject`
        The scene object associated with the node.

    Attributes
    ----------
    name : str
        The name of the node, same as the underlying scene object.
    object : :class:`compas.scene.SceneObject`
        The scene object associated with the node.
    parentobject : :class:`compas.scene.SceneObject`
        The scene object associated with the parent node.
    childobjects : list[:class:`compas.scene.SceneObject`]
        The scene objects associated with the child nodes.

    """

    @property
    def __data__(self):
        return {
            "item": str(self.object.item.guid),
            "settings": self.object.settings,
            "children": [child.__data__ for child in self.children],
        }

    @classmethod
    def __from_data__(cls, data):
        raise TypeError("SceneObjectNode cannot be created from data. Use Scene.__from_data__ instead.")

    def __init__(self, sceneobject, name=None):
        super(SceneObjectNode, self).__init__(name=name)
        self.object = sceneobject

    @property
    def name(self):
        if self.object:
            return self.object.name

    @property
    def parentobject(self):
        if self.parent and isinstance(self.parent, SceneObjectNode):
            return self.parent.object
        return None

    @property
    def childobjects(self):
        return [child.object for child in self.children]

    def add_item(self, item, **kwargs):
        """Add an child item to the node.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            The item to add.
        **kwargs : dict
            Additional keyword arguments to create the scene object for the item.

        Returns
        -------
        :class:`compas.scene.SceneObject`
            The scene object associated with the item.

        """
        sceneobject = SceneObject(item, **kwargs)
        node = SceneObjectNode(sceneobject)
        self.add(node)
        sceneobject._node = node  # type: ignore
        return sceneobject


class SceneTree(Tree):
    """A tree structure for storing the hierarchy of scene objects in a scene. The SceneTree should only be used internally by the Scene.

    Parameters
    ----------
    name : str, optional
        The name of the tree.

    Attributes
    ----------
    objects : list[:class:`compas.scene.SceneObject`]
        All scene objects in the scene tree.

    """

    @classmethod
    def __from_data__(cls, data):
        raise TypeError("SceneTree cannot be created from data. Use Scene.__from_data__ instead.")

    def __init__(self, name=None):
        super(SceneTree, self).__init__(name=name)
        root = TreeNode(name="root")
        self.add(root)

    @property
    def objects(self):
        return [node.object for node in self.nodes if isinstance(node, SceneObjectNode)]

    def add_object(self, sceneobject, parent=None):
        """Add a scene object to the tree.

        Parameters
        ----------
        sceneobject : :class:`compas.scene.SceneObject`
            The scene object to add.
        parent : :class:`compas.scene.SceneObject`, optional
            The parent scene object.

        Returns
        -------
        :class:`compas.scene.SceneObjectNode`
            The node associated with the scene object.

        """
        node = SceneObjectNode(sceneobject)
        if parent is None:
            self.add(node, parent=self.root)
        else:
            parent_node = self.get_node_from_object(parent)
            self.add(node, parent=parent_node)

        sceneobject._node = node
        return node

    def remove_object(self, sceneobject):
        """Remove a scene object from the tree.

        Parameters
        ----------
        sceneobject : :class:`compas.scene.SceneObject`
            The scene object to remove.

        """
        node = self.get_node_from_object(sceneobject)
        self.remove(node)

    def get_node_from_object(self, sceneobject):
        """Get the node associated with a scene object.

        Parameters
        ----------
        sceneobject : :class:`compas.scene.SceneObject`
            The scene object.

        Returns
        -------
        :class:`compas.scene.SceneObjectNode`
            The node associated with the scene object.

        Raises
        ------
        ValueError
            If the scene object is not in the scene tree.

        """
        for node in self.nodes:
            if isinstance(node, SceneObjectNode):
                if node.object is sceneobject:
                    return node
        raise ValueError("Scene object not in scene tree")


class Scene(Data):
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
    >>> scene.add(box)
    >>> scene.redraw()

    """

    viewerinstance = None

    @property
    def __data__(self):
        items = {str(object.item.guid): object.item for object in self.objects}
        return {
            "name": self.name,
            "tree": self.tree.__data__,
            "items": list(items.values()),
        }

    @classmethod
    def __from_data__(cls, data):
        scene = cls(data["name"])
        items = {str(item.guid): item for item in data["items"]}

        def add(node, parent, items):
            for child_node in node["children"]:
                guid = child_node["item"]
                settings = child_node["settings"]
                sceneobject = parent.add(items[guid], **settings)
                add(child_node, sceneobject, items)

        add(data["tree"]["root"], scene, items)

        return scene

    def __init__(self, name=None, context=None):
        super(Scene, self).__init__(name)
        self._tree = SceneTree("Scene")
        self.context = context or detect_current_context()

    @property
    def tree(self):
        return self._tree

    @property
    def objects(self):
        return self.tree.objects

    def add(self, item, parent=None, **kwargs):
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
        sceneobject = SceneObject(item, context=self.context, **kwargs)
        self.tree.add_object(sceneobject, parent=parent)
        return sceneobject

    def remove(self, sceneobject):
        """Remove a scene object from the scene.

        Parameters
        ----------
        sceneobject : :class:`compas.scene.SceneObject`
            The scene object to remove.

        """
        self.tree.remove_object(sceneobject)

    def clear(self):
        """Clear the current context of the scene."""
        clear()

    def clear_objects(self):
        """Clear all objects inside the scene."""
        guids = []
        for sceneobject in self.objects:
            guids += sceneobject.guids
            sceneobject._guids = None
        clear(guids=guids)

    def redraw(self):
        """Redraw the scene."""

        if not self.context:
            raise ValueError("No context detected.")

        self.clear_objects()

        drawn_objects = []
        for sceneobject in self.objects:
            drawn_objects += sceneobject.draw()

        if drawn_objects:
            redraw()

        return drawn_objects

    def print_hierarchy(self):
        """Print the hierarchy of the scene."""
        self.tree.print_hierarchy()
