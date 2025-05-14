from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import reduce
from operator import mul

import compas.colors  # noqa: F401
import compas.data  # noqa: F401
import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
import compas.scene  # noqa: F401
from compas.colors import Color
from compas.data import Data
from compas.geometry import Frame
from compas.geometry import Transformation

from .context import clear
from .context import get_sceneobject_cls
from .descriptors.color import ColorAttribute
from .descriptors.protocol import DescriptorProtocol


class SceneObjectFactory:
    """Factory class for creating appropriate SceneObject instances based on input item type.

    This factory encapsulates the logic for selecting the right SceneObject subclass
    for a given data item, making the creation process more explicit and easier to understand.
    """

    @staticmethod
    def create(item=None, scene=None, **kwargs):
        """Create appropriate SceneObject instance based on item type.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            The data item to create a scene object for.
        **kwargs : dict
            Additional keyword arguments to pass to the SceneObject constructor.

        Returns
        -------
        :class:`compas.scene.SceneObject`
            A SceneObject instance of the appropriate subclass for the given item.

        Raises
        ------
        ValueError
            If item is None.
        SceneObjectNotRegisteredError
            If no scene object is registered for the item type in the current context.
        """
        if item is None:
            raise ValueError("Cannot create a scene object for None. Please ensure you pass an instance of a supported class.")

        if isinstance(item, SceneObject):
            item._scene = scene
            return item

        sceneobject_cls = get_sceneobject_cls(item, **kwargs)

        # Create and return an instance of the appropriate scene object class
        return sceneobject_cls(item=item, scene=scene, **kwargs)


class SceneObject(Data):
    """Base class for all scene objects.

    Parameters
    ----------
    item : Any
        The item which should be visualized using the created SceneObject.
    name : str, optional
        The name of the scene object. Note that is is not the same as the name of underlying data item, since different scene objects can refer to the same data item.
    color : :class:`compas.colors.Color`, optional
        The color of the object.
    opacity : float, optional
        The opacity of the object.
    show : bool, optional
        Flag for showing or hiding the object. Default is ``True``.
    transformation : :class:`compas.geometry.Transformation`, optional
        The local transformation of the scene object in relation to its parent object.
    context : str, optional
        The context in which the scene object is created.
    **kwargs : dict
        Additional keyword arguments to create the scene object for the item.

    Attributes
    ----------
    item : :class:`compas.data.Data`
        The item which should be visualized using the created SceneObject.
    name : str
        The name of the scene object. Note that is is not the same as the name of underlying data item, since different scene objects can refer to the same data item.
    node : :class:`compas.scene.SceneObjectNode`
        The node in the scene tree which represents the scene object.
    guids : list[object]
        The GUIDs of the items drawn in the visualization context.
    transformation : :class:`compas.geometry.Transformation`
        The local transformation of the scene object in relation to its parent object.
    worldtransformation : :class:`compas.geometry.Transformation`
        The global transformation of the scene object in world coordinates, computed by multiplying all transformations from the scene object to the root of the scene tree.
        (NOTE: Changed from 2.11.0, there will no longer be the option of additional transformation in relation to the object's frame)
    frame : :class:`compas.geometry.Frame`
        The frame of the local coordinate system of the scene object, derived from the `worldtransformation`.
    color : :class:`compas.colors.Color`
        The color of the object.
    contrastcolor : :class:`compas.colors.Color`, readon-only
        The contrastcolor wrt to the color.
        This is a 50% darket or lighter version of the color, depending on whether the color is light or dark.
    opacity : float
        The opacity of the object.
    show : bool
        Flag for showing or hiding the object. Default is ``True``.
    settings : dict
        The settings including necessary attributes for reconstructing the scene object besides the Data item.
    context : str
        The context in which the scene object is created.
    scene : :class:`compas.scene.Scene`
        The scene to which the scene object belongs.

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    color = ColorAttribute()

    def __init__(
        self,
        item=None,  # type: compas.data.Data | None
        name=None,  # type: str | None
        color=None,  # type: compas.colors.Color | None
        opacity=1.0,  # type: float
        show=True,  # type: bool
        transformation=None,  # type: compas.geometry.Transformation | None
        context=None,  # type: str | None
        scene=None,  # type: compas.scene.Scene | None
        **kwargs  # type: dict
    ):  # fmt: skip
        # type: (...) -> None

        name = name or getattr(item, "name", None)
        super(SceneObject, self).__init__(name=name, **kwargs)
        # the scene object needs to store the context
        # because it has no access to the tree and/or the scene before it is added
        # which means that adding child objects will be added in context "None"

        if isinstance(item, Data):
            self._item = str(item.guid)
        elif isinstance(item, str):
            self._item = item
        elif item is None:
            self._item = None
        else:
            raise ValueError("The item assigned to this scene object should be a data object or a str guid: {}".format(item))

        self.context = context
        self._scene = scene
        self._guids = []
        self._node = None
        self._transformation = transformation
        self._contrastcolor = None
        self.color = color or self.color
        self.opacity = opacity
        self.show = show

    @property
    def __data__(self):
        # type: () -> dict
        return {
            "item": self._item,
            "name": self.name,
            "color": self.color,
            "opacity": self.opacity,
            "show": self.show,
            "transformation": self.transformation,
        }

    def __repr__(self):
        # type: () -> str
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    @property
    def scene(self):
        # type: () -> compas.scene.Scene | None
        return self._scene

    @property
    def item(self):
        # type: () -> compas.data.Data
        return self.scene.items[self._item]

    @property
    def node(self):
        # type: () -> compas.datastructures.TreeNode
        return self.scene.tree.get_node_by_name(self.guid)

    @property
    def is_root(self):
        # type: () -> bool
        return self.node.is_root

    @property
    def is_leaf(self):
        # type: () -> bool
        return self.node.is_leaf

    @property
    def is_branch(self):
        # type: () -> bool
        return self.node.is_branch

    @property
    def parentnode(self):
        # type: () -> compas.datastructures.Node | None
        return self.node.parent

    @property
    def childnodes(self):
        # type: () -> list[compas.datastructures.Node]
        return self.node.children

    @property
    def parent(self):
        # type: () -> compas.scene.SceneObject | None
        if self.parentnode and not self.parentnode.is_root:
            return self.scene.objects[self.parentnode.name]
        return None

    @property
    def children(self):
        # type: () -> list[compas.scene.SceneObject]
        return [self.scene.objects[child.name] for child in self.childnodes]

    @property
    def guids(self):
        # type: () -> list[str]
        return self._guids or []

    @property
    def frame(self):
        # type: () -> compas.geometry.Frame | None
        return Frame.from_transformation(self.worldtransformation)

    @property
    def transformation(self):
        # type: () -> compas.geometry.Transformation | None
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        # type: (compas.geometry.Transformation) -> None
        self._transformation = transformation

    @property
    def worldtransformation(self):
        # type: () -> compas.geometry.Transformation
        transformations = [self.transformation] if self.transformation else []
        parent = self.parent
        while parent and not parent.is_root:
            if parent.transformation:
                transformations.append(parent.transformation)
            parent = parent.parent
        if transformations:
            worldtransformation = reduce(mul, transformations[::-1])
        else:
            worldtransformation = Transformation()

        return worldtransformation

    @property
    def contrastcolor(self):
        # type: () -> compas.colors.Color | None
        if not self._contrastcolor:
            if self.color:
                if self.color.is_light:
                    self._contrastcolor = self.color.darkened(50)
                else:
                    self._contrastcolor = self.color.lightened(50)
        return self._contrastcolor

    def add(self, item, **kwargs):
        """Add a scene object to the scene.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            The item to add to the scene.
        **kwargs : dict
            Additional keyword arguments to pass to the SceneObject constructor.

        Returns
        -------
        :class:`compas.scene.SceneObject`
            The added scene object.
        """
        # type: (compas.data.Data, dict) -> compas.scene.SceneObject
        return self.scene.add(item, parent=self, **kwargs)

    def remove(self):
        """Remove this scene object along with all its descendants from the scene."""
        self.scene.remove(self)

    @contrastcolor.setter
    def contrastcolor(self, color):
        # type: (compas.colors.Color) -> None
        self._contrastcolor = Color.coerce(color)

    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    def clear(self):
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None
