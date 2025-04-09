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
from compas.datastructures import TreeNode
from compas.geometry import Frame
from compas.geometry import Transformation

from .context import clear
from .context import get_sceneobject_cls
from .descriptors.color import ColorAttribute
from .descriptors.protocol import DescriptorProtocol


class SceneObject(TreeNode):
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

    def __new__(cls, item=None, **kwargs):
        sceneobject_cls = get_sceneobject_cls(item, **kwargs)
        return super(SceneObject, cls).__new__(sceneobject_cls)

    def __init__(
        self,
        item=None,  # type: compas.data.Data | None
        name=None,  # type: str | None
        color=None,  # type: compas.colors.Color | None
        opacity=1.0,  # type: float
        show=True,  # type: bool
        frame=None,  # type: compas.geometry.Frame | None
        transformation=None,  # type: compas.geometry.Transformation | None
        context=None,  # type: str | None
        **kwargs  # type: dict
    ):  # fmt: skip
        # type: (...) -> None
        if item and not isinstance(item, Data):
            raise ValueError("The item assigned to this scene object should be a data object: {}".format(type(item)))

        name = name or getattr(item, "name", None)
        super(SceneObject, self).__init__(name=name, **kwargs)
        # the scene object needs to store the context
        # because it has no access to the tree and/or the scene before it is added
        # which means that adding child objects will be added in context "None"
        self.context = context
        self._item = item
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
            "item": str(self.item.guid),
            "settings": self.settings,
            "children": [child.__data__ for child in self.children],
        }

    @classmethod
    def __from_data__(cls, data):
        # type: (dict) -> None
        raise TypeError("Serialisation outside Scene not allowed.")

    def __repr__(self):
        # type: () -> str
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    @property
    def scene(self):
        # type: () -> compas.scene.Scene | None
        return self.tree

    @property
    def item(self):
        # type: () -> compas.data.Data
        return self._item

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

    @contrastcolor.setter
    def contrastcolor(self, color):
        # type: (compas.colors.Color) -> None
        self._contrastcolor = Color.coerce(color)

    @property
    def settings(self):
        # type: () -> dict
        settings = {
            "name": self.name,
            "color": self.color,
            "opacity": self.opacity,
            "show": self.show,
        }

        if self.frame:
            settings["frame"] = self.frame
        if self.transformation:
            settings["transformation"] = self.transformation

        return settings

    def add(self, item, **kwargs):
        # type: (compas.data.Data, dict) -> SceneObject
        """Add a child item to the scene object.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            The item to add.
        **kwargs : dict
            Additional keyword arguments to create the scene object for the item.

        Returns
        -------
        :class:`compas.scene.SceneObject`
            The scene object associated with the added item.

        Raises
        ------
        ValueError
            If the scene object does not have an associated scene node.
        """
        if isinstance(item, SceneObject):
            sceneobject = item
        else:
            if "context" in kwargs:
                if kwargs["context"] != self.context:
                    raise Exception("Child context should be the same as parent context: {} != {}".format(kwargs["context"], self.context))
                del kwargs["context"]  # otherwist the SceneObject receives "context" twice, which results in an error
            sceneobject = SceneObject(item=item, context=self.context, **kwargs)  # type: ignore

        super(SceneObject, self).add(sceneobject)
        return sceneobject

    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    def clear(self):
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None
