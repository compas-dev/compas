from functools import reduce
from operator import mul
from typing import TYPE_CHECKING
from typing import Any
from typing import NoReturn
from typing import Self
from typing import cast

from compas.colors import Color
from compas.data import Data
from compas.datastructures import TreeNode
from compas.geometry import Frame
from compas.geometry import Transformation

from .context import clear
from .context import get_sceneobject_cls
from .descriptors.color import ColorAttribute

if TYPE_CHECKING:
    from compas.scene import Scene


class SceneObject(TreeNode["SceneObject"]):
    """Base class for all scene objects.

    Parameters
    ----------
    item
        The item to visualize.
    name
        The name of the scene object. This is independent of the name of the
        underlying data item because multiple scene objects can refer to the
        same item.
    color
        The color of the object.
    opacity
        The opacity of the object.
    show
        Whether to show the object.
    transformation
        The local transformation relative to the parent scene object.
    context
        The context in which the scene object is created.
    **kwargs
        Additional keyword arguments to create the scene object for the item.

    Notes
    -----
    `SceneObject(...)` may dispatch to a registered subclass. The internal
    `sceneobject_type` factory override is accepted by `__new__`, but is not an
    initialization parameter of constructed scene objects.

    """

    color = ColorAttribute()

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict[str, object]:
        if self.item is None:
            raise ValueError("A scene object without an item cannot be serialized independently.")
        return {
            "item": str(self.item.guid),
            "settings": self.settings,
            "children": [child.__data__ for child in self.children],
        }

    @classmethod
    def __from_data__(cls, data: dict[str, object]) -> NoReturn:
        raise TypeError("Serialisation outside Scene not allowed.")

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __new__(
        cls,
        item: Data | None = None,
        context: str | None = None,
        sceneobject_type: type["SceneObject"] | None = None,
        **kwargs: Any,
    ) -> Self:
        sceneobject_cls = get_sceneobject_cls(item, context=context, sceneobject_type=sceneobject_type, **kwargs)
        return cast(Self, object.__new__(sceneobject_cls))

    def __init__(
        self,
        item: Data | None = None,
        name: str | None = None,
        color: Color | None = None,
        opacity: float = 1.0,
        show: bool = True,
        transformation: Transformation | None = None,
        context: str | None = None,
        **kwargs: object,
    ) -> None:
        if item and not isinstance(item, Data):
            raise ValueError("The item assigned to this scene object should be a data object: {}".format(type(item)))

        # This factory-only option has already been handled by __new__.
        kwargs.pop("sceneobject_type", None)
        name = name or getattr(item, "name", None)
        super().__init__(name=name, **kwargs)
        # the scene object needs to store the context
        # because it has no access to the tree and/or the scene before it is added
        # which means that adding child objects will be added in context "None"
        self.context = context
        self._item = item
        self._scene: Scene | None = None
        self._guids: list[object] | None = []
        self._node = None
        self._transformation = transformation
        self._transformation_revision = 0
        self._contrastcolor = None
        self.color = color or self.color
        self.opacity = opacity
        self.show = show

    def __repr__(self) -> str:
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def scene(self) -> "Scene | None":
        """The scene containing this object, if it has been added to one."""
        return self._scene

    @property
    def item(self) -> Data | None:
        """The data item represented by this scene object."""
        return self._item

    @property
    def guids(self) -> list[object]:
        """The identifiers of objects created in the visualization context."""
        return self._guids or []

    @property
    def frame(self) -> Frame:
        """The frame represented by the world transformation.

        Setting the frame updates the local transformation relative to the
        parent scene object.

        """
        return Frame.from_transformation(self.worldtransformation)

    @frame.setter
    def frame(self, frame: Frame) -> None:
        self.worldtransformation = Transformation.from_frame(frame)

    @property
    def transformation(self) -> Transformation | None:
        """The local transformation relative to the parent scene object.

        Setting the transformation invalidates transformation-dependent caches
        on this object. Descendant caches detect the change lazily.

        """
        return self._transformation

    @transformation.setter
    def transformation(self, transformation: Transformation | None) -> None:
        self._transformation = transformation
        self._transformation_revision += 1
        self.invalidate()

    @property
    def worldtransformation(self) -> Transformation:
        """The transformation from local coordinates to world coordinates.

        The transformation is computed from this object's local transformation
        and those of its ancestors. Setting it derives the corresponding local
        transformation relative to the parent.

        """
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

    @worldtransformation.setter
    def worldtransformation(self, worldtransformation: Transformation) -> None:
        if isinstance(self.parent, SceneObject):
            self.transformation = self.parent.worldtransformation.inverse() * worldtransformation
        else:
            self.transformation = worldtransformation

    @property
    def contrastcolor(self) -> Color | None:
        """A lighter or darker color contrasting with the object color.

        The computed color is cached. Setting this property coerces the value to
        a `Color`.

        """
        if not self._contrastcolor:
            if self.color:
                if self.color.is_light:
                    self._contrastcolor = self.color.darkened(50)
                else:
                    self._contrastcolor = self.color.lightened(50)
        return self._contrastcolor

    @contrastcolor.setter
    def contrastcolor(self, color: Color) -> None:
        self._contrastcolor = Color.coerce(color)

    @property
    def settings(self) -> dict[str, object]:
        """The settings required to reconstruct the scene object."""
        settings = {
            "name": self.name,
            "color": self.color,
            "opacity": self.opacity,
            "show": self.show,
        }

        if self.transformation:
            settings["transformation"] = self.transformation

        return settings

    # ==========================================================================
    # Methods
    # ==========================================================================

    def invalidate(self) -> None:
        """Clear cached data derived from the represented item or transformation.

        Call this after mutating an underlying item through a path that the scene
        object cannot observe directly. Descendants detect ancestor
        transformation changes automatically and do not need to be invalidated.

        """
        self._invalidate_transformation_cache()

    def add(self, item: Data, **kwargs: Any) -> "SceneObject":
        """Add a child item to the scene object.

        Parameters
        ----------
        item
            The item to add.
        **kwargs
            Additional keyword arguments to create the scene object for the item.

        Returns
        -------
        SceneObject
            The scene object associated with the added item.

        """
        if self.scene is not None:
            return self.scene.add(item, parent=self, **kwargs)

        if isinstance(item, SceneObject):
            sceneobject = item
        else:
            if "context" in kwargs:
                if kwargs["context"] != self.context:
                    raise Exception("Child context should be the same as parent context: {} != {}".format(kwargs["context"], self.context))
                del kwargs["context"]  # otherwist the SceneObject receives "context" twice, which results in an error
            sceneobject = SceneObject(item=item, context=self.context, **kwargs)

        super().add(sceneobject)
        return sceneobject

    def draw(self) -> list[object]:
        """The main drawing method."""
        raise NotImplementedError

    def clear(self) -> None:
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None

    # ==========================================================================
    # Private helpers
    # ==========================================================================

    def _invalidate_transformation_cache(self) -> None:
        """Invalidate cached data derived from the local transformation.

        Scene object types with transformation-dependent caches override this
        hook. The base scene object has no such cache.

        """
        pass

    def _worldtransformation_revision(self) -> tuple[int, ...]:
        """Return the revisions that determine the current world transformation."""
        revisions = [self._transformation_revision]
        parent = self.parent
        while parent and not parent.is_root:
            revisions.append(parent._transformation_revision)
            parent = parent.parent
        return tuple(reversed(revisions))
