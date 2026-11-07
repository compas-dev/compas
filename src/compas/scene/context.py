import inspect
from collections.abc import Callable
from typing import TYPE_CHECKING
from typing import Any

from compas.data import Data
from compas.plugins import pluggable

from .exceptions import SceneObjectNotRegisteredError
from .exceptions import SceneOperationNotRegisteredError

if TYPE_CHECKING:
    from .sceneobject import SceneObject


SCENEOBJECT_TYPES: dict[type[Data], type["SceneObject"]] = {}
SCENE_OPERATIONS: dict[str, dict[type["SceneObject"], dict[str, Callable[..., Any]]]] = {}
_SCENEOBJECTS_DISCOVERED = False
_OPERATIONS_DISCOVERED = False


@pluggable(category="factories", selector="collect_all")
def register_scene_objects() -> None:
    """Register stable semantic scene-object types."""
    raise NotImplementedError


@pluggable(category="factories", selector="collect_all")
def register_scene_operations() -> None:
    """Register context-specific scene operations."""
    raise NotImplementedError


def register_sceneobject_type(item_type: type[Data], sceneobject_type: type["SceneObject"]) -> None:
    """Register the stable scene-object type for a data type.

    Parameters
    ----------
    item_type
        The represented data type.
    sceneobject_type
        Its stable semantic scene-object type.

    Raises
    ------
    ValueError
        If another scene-object type is already registered for `item_type`.

    """
    existing = SCENEOBJECT_TYPES.get(item_type)
    if existing is not None and existing is not sceneobject_type:
        raise ValueError(f"A scene-object type is already registered for {item_type.__name__}.")
    SCENEOBJECT_TYPES[item_type] = sceneobject_type


def get_sceneobject_cls(item: Data) -> type["SceneObject"]:
    """Return the stable semantic scene-object type for an item.

    Parameters
    ----------
    item
        The represented data item.

    Returns
    -------
    type[SceneObject]

    Raises
    ------
    SceneObjectNotRegisteredError
        If no compatible stable type is registered.

    """
    _ensure_sceneobjects_discovered()
    for item_type in inspect.getmro(type(item)):
        sceneobject_type = SCENEOBJECT_TYPES.get(item_type)
        if sceneobject_type is not None:
            return sceneobject_type
    raise SceneObjectNotRegisteredError(f"No stable scene-object type is registered for {type(item).__name__}.")


def register_scene_operation(
    context: str,
    sceneobject_type: type["SceneObject"],
    operation: str,
    implementation: Callable[..., Any],
) -> None:
    """Register one context-specific scene operation.

    Parameters
    ----------
    context
        Stable visualization-context name.
    sceneobject_type
        Stable scene-object type accepted by the implementation.
    operation
        Operation name. Initially only `draw` and `clear` are supported.
    implementation
        Operation function.

    Raises
    ------
    ValueError
        If the key is invalid or already has another implementation.

    """
    if not context:
        raise ValueError("A scene-operation context should be a non-empty string.")
    if operation not in {"draw", "clear"}:
        raise ValueError("A scene operation should be 'draw' or 'clear'.")
    operations = SCENE_OPERATIONS.setdefault(context, {}).setdefault(sceneobject_type, {})
    existing = operations.get(operation)
    if existing is not None and existing is not implementation:
        raise ValueError(f"Scene operation already registered: {context}/{sceneobject_type.__name__}/{operation}.")
    operations[operation] = implementation


def get_scene_operation(context: str, sceneobject_type: type["SceneObject"], operation: str) -> Callable[..., Any]:
    """Resolve a scene operation using stable-type MRO fallback.

    Parameters
    ----------
    context
        Visualization-context name.
    sceneobject_type
        Concrete stable scene-object type.
    operation
        Operation name.

    Returns
    -------
    Callable[..., Any]

    Raises
    ------
    SceneOperationNotRegisteredError
        If the context has no compatible implementation.

    """
    _ensure_operations_discovered()
    registry = SCENE_OPERATIONS.get(context, {})
    for candidate in inspect.getmro(sceneobject_type):
        implementation = registry.get(candidate, {}).get(operation)
        if implementation is not None:
            return implementation
    raise SceneOperationNotRegisteredError(context, sceneobject_type, operation)


def detect_current_context() -> str | None:
    """Return the only registered visualization context, if unambiguous."""
    _ensure_operations_discovered()
    contexts = [context for context, registry in SCENE_OPERATIONS.items() if registry]
    return contexts[0] if len(contexts) == 1 else None


def _ensure_sceneobjects_discovered() -> None:
    global _SCENEOBJECTS_DISCOVERED
    if not _SCENEOBJECTS_DISCOVERED:
        register_scene_objects()
        _SCENEOBJECTS_DISCOVERED = True


def _ensure_operations_discovered() -> None:
    global _OPERATIONS_DISCOVERED
    if not _OPERATIONS_DISCOVERED:
        register_scene_operations()
        _OPERATIONS_DISCOVERED = True
