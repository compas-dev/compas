class SceneObjectNotRegisteredError(Exception):
    """Exception that is raised when no scene object is registered for a given data type."""


class SceneItemNotBoundError(LookupError):
    """Raised when an operation requires an unresolved scene item reference."""

    def __init__(self, object_guid: object, item_guid: object) -> None:
        super().__init__(f"Scene object {object_guid} requires unbound item {item_guid}.")
        self.object_guid = object_guid
        self.item_guid = item_guid


class SceneStateError(ValueError):
    """Raised when declared durable scene state is invalid."""


class SceneOperationNotRegisteredError(LookupError):
    """Raised when a visualization context has no compatible operation."""

    def __init__(self, context: str, sceneobject_type: type[object], operation: str) -> None:
        super().__init__(f"No '{operation}' scene operation is registered for {sceneobject_type.__name__} in context '{context}'.")
        self.context = context
        self.sceneobject_type = sceneobject_type
        self.operation = operation
