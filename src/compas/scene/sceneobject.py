from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod
from .descriptors.protocol import DescriptorProtocol
from .descriptors.color import ColorAttribute
from .context import clear
from .context import get_sceneobject_cls
from compas.geometry import Transformation
from functools import reduce
from operator import mul


class SceneObject(object):
    """Base class for all scene objects.

    Parameters
    ----------
    item : Any
        The item which should be visualized using the created SceneObject.
    **kwargs : dict
        Additional keyword arguments for constructing SceneObject.

    Attributes
    ----------
    item : :class:`compas.data.Data`
        The item which should be visualized using the created SceneObject.
    node : :class:`compas.scene.SceneObjectNode`
        The node in the scene tree which represents the scene object.
    guids : list[object]
        The GUIDs of the items drawn in the visualization context.
    parent : :class:`compas.scene.SceneObject`
        The parent scene object.
    children : list[:class:`compas.scene.SceneObject`]
        The child scene objects.
    frame : :class:`compas.geometry.Frame`
        The local frame of the scene object, in relation to its parent frame.
    transformation : :class:`compas.geometry.Transformation`
        The local transformation of the scene object in relation to its frame.
    worldtransformation : :class:`compas.geometry.Transformation`
        The transformation of the scene object in world coordinates.
    color : :class:`compas.colors.Color`
        The color of the object.
    opacity : float
        The opacity of the object.
    settings : dict
        The settings including necessary attributes for reconstructing the scene object.

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    color = ColorAttribute()

    def __new__(cls, item, **kwargs):
        sceneobject_cls = get_sceneobject_cls(item, **kwargs)
        return super(SceneObject, cls).__new__(sceneobject_cls)

    def __init__(self, item, **kwargs):
        self._item = item
        self._guids = None
        self._node = None
        self._frame = kwargs.get("frame", None)
        self._transformation = kwargs.get("transformation", None)
        self.name = kwargs.get("name", item.name or item.__class__.__name__)
        self.color = kwargs.get("color", self.color)
        self.opacity = kwargs.get("opacity", 1.0)

    @property
    def item(self):
        return self._item

    @property
    def guids(self):
        return self._guids or []

    @property
    def node(self):
        return self._node

    @property
    def parent(self):
        if self.node:
            return self.node.parentobject

    @property
    def children(self):
        if self.node:
            return self.node.childobjects
        else:
            return []

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame

    @property
    def transformation(self):
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._transformation = transformation

    @property
    def worldtransformation(self):
        frame_stack = []
        parent = self.parent
        while parent:
            if parent.frame:
                frame_stack.append(parent.frame)
            parent = parent.parent
        matrices = [Transformation.from_frame(f) for f in frame_stack]
        if matrices:
            worldtransformation = reduce(mul, matrices[::-1])
        else:
            worldtransformation = Transformation()

        if self.transformation:
            worldtransformation *= self.transformation

        return worldtransformation

    def add(self, item, **kwargs):
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
        if self.node:
            return self.node.add_item(item, **kwargs)
        else:
            raise ValueError("Cannot add items to a scene object without a node.")

    @property
    def settings(self):
        return {
            "name": self.name,
            "color": self.color,
            "opacity": self.opacity,
            "frame": self.frame,
            "transformation": self.transformation,
        }

    @abstractmethod
    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    def clear(self):
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None
