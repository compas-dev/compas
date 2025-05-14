import compas.data  # noqa: F401
import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
from compas.datastructures import Datastructure
from compas.datastructures import Tree
from compas.datastructures import TreeNode

from .context import after_draw
from .context import before_draw
from .context import clear
from .context import detect_current_context
from .sceneobject import SceneObject
from .sceneobject import SceneObjectFactory


class Scene(Datastructure):
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
        return {
            "name": self.name,
            "attributes": self.attributes,
            "datastore": self.datastore,
            "objectstore": self.objectstore,
            "tree": self.tree,
        }

    def __init__(self, context=None, datastore=None, objectstore=None, tree=None, **kwargs):
        # type: (str | None, dict | None, dict | None, Tree | None, **kwargs) -> None
        super(Scene, self).__init__(**kwargs)

        self.context = context or detect_current_context()
        self.datastore = datastore or {}
        self.objectstore = objectstore or {}
        self.tree = tree or Tree()
        if self.tree.root is None:
            self.tree.add(TreeNode(name=self.name))

    def __repr__(self):
        # type: () -> str

        def node_repr(node):
            # type: (TreeNode) -> str
            if node.is_root:
                return node.name
            else:
                sceneobject = self.objectstore[node.name]
                return str(sceneobject)

        return self.tree.get_hierarchy_string(node_repr=node_repr)

    @property
    def items(self):
        # type: () -> list
        return list(self.datastore.values())

    @property
    def objects(self):
        # type: () -> list
        return list(self.objectstore.values())

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

        # Create a corresponding new scene object
        sceneobject = SceneObjectFactory.create(item=item, context=self.context, scene=self, **kwargs)

        # Add the scene object and item to the data store
        self.objectstore[str(sceneobject.guid)] = sceneobject
        self.datastore[str(item.guid)] = item

        # Add the scene object to the hierarchical tree
        if parent is None:
            parent_node = self.tree.root
        else:
            if not isinstance(parent, SceneObject):
                raise ValueError("Parent is not a SceneObject.", parent)
            parent_node = self.tree.get_node_by_name(parent.guid)
            if parent_node is None:
                raise ValueError("Parent is not part of the scene.", parent)

        self.tree.add(TreeNode(name=str(sceneobject.guid)), parent=parent_node)

        return sceneobject

    def remove(self, sceneobject):
        """Remove a scene object along with all its descendants from the scene.

        Parameters
        ----------
        sceneobject : :class:`compas.scene.SceneObject`
            The scene object to remove.
        """
        # type: (SceneObject) -> None
        guid = str(sceneobject.guid)
        self.objectstore.pop(guid, None)
        node = self.tree.get_node_by_name(guid)
        if node:
            for descendant in node.descendants:
                self.objectstore.pop(descendant.name, None)
            self.tree.remove(node)

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
        # type: (type) -> SceneObject | None
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
        # type: (type) -> list[SceneObject]
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
