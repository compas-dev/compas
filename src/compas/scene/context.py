import inspect
from collections import defaultdict
from typing import TYPE_CHECKING

from compas.data import Data
from compas.plugins import pluggable
from compas.plugins import validate_plugin_implementation

from .exceptions import SceneObjectNotRegisteredError

if TYPE_CHECKING:
    from .sceneobject import SceneObject

ITEM_SCENEOBJECT: defaultdict[str | None, dict[type[Data], type["SceneObject"]]] = defaultdict(dict)


@pluggable(category="drawing-utils")
def clear(guids: list[object] | None = None) -> None:
    """Clear all or selected objects from the current visualization context.

    Parameters
    ----------
    guids
        The identifiers to clear. If `None`, clear the entire context.

    """
    raise NotImplementedError


@pluggable(category="drawing-utils")
def before_draw() -> None:
    """Perform context-specific operations before drawing a scene."""
    pass


@pluggable(category="drawing-utils")
def after_draw(drawn_objects: list[object]) -> None:
    """Perform context-specific operations after drawing a scene.

    Parameters
    ----------
    drawn_objects
        The objects that were drawn.

    """
    pass


@pluggable(category="factories", selector="collect_all")
def register_scene_objects() -> None:
    """Register scene object types available in the current context."""
    raise NotImplementedError


def register(item_type: type[Data], sceneobject_type: "type[SceneObject]", context: str | None = None) -> None:
    """Register a scene object type to a data type.

    Parameters
    ----------
    item_type
        The type of data item.
    sceneobject_type
        The compatible scene object type.
    context
        The visualization context in which to register the pair.

    """
    ITEM_SCENEOBJECT[context][item_type] = sceneobject_type


def detect_current_context() -> str | None:
    """Select the only registered named visualization context, if available.

    Returns
    -------
    str | None
        The context name when exactly one named context is registered.
        Otherwise, `None`.

    """

    contexts = [name for name, registry in ITEM_SCENEOBJECT.items() if name is not None and registry]
    return contexts[0] if len(contexts) == 1 else None


def _get_sceneobject_cls(
    data: Data,
    context: str | None = None,
    sceneobject_type: "type[SceneObject] | None" = None,
) -> "type[SceneObject]":
    # in any case user gets to override the choice
    context_name = context or detect_current_context()

    dtype = type(data)
    cls = None

    if sceneobject_type is not None:
        cls = sceneobject_type
    else:
        registry = ITEM_SCENEOBJECT[context_name]

        for type_ in inspect.getmro(dtype):
            cls = registry.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise SceneObjectNotRegisteredError("No scene object is registered for this data type: {} in this context: {}".format(dtype, context_name))

    return cls


def get_sceneobject_cls(
    item: Data | None,
    context: str | None = None,
    sceneobject_type: "type[SceneObject] | None" = None,
    **kwargs: object,
) -> "type[SceneObject]":
    """Get the registered scene object type for an item.

    Parameters
    ----------
    item
        The item to represent.
    context
        The visualization context used for registration lookup.
    sceneobject_type
        An explicit scene object type overriding registration lookup.
    **kwargs
        Additional scene object options, ignored during type selection.

    Returns
    -------
    type[SceneObject]
        The selected scene object type.

    Raises
    ------
    ValueError
        If `item` is `None`.
    SceneObjectNotRegisteredError
        If no compatible scene object type is registered.

    """
    if not ITEM_SCENEOBJECT:
        register_scene_objects()

    if item is None:
        raise ValueError("Cannot create a scene object for None. Please ensure you pass a instance of a supported class.")

    cls = _get_sceneobject_cls(item, context=context, sceneobject_type=sceneobject_type)
    validate_plugin_implementation(cls)
    return cls
