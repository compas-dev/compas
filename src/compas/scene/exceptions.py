class SceneObjectNotRegisteredError(Exception):
    """Exception that is raised when no scene object is registered for a given data type."""


class SceneItemNotBoundError(LookupError):
    """Raised when an operation requires an unresolved scene item reference."""

    def __init__(self, node_guid: object, item_guid: object) -> None:
        super().__init__(f"Scene node {node_guid} requires unbound item {item_guid}.")
        self.node_guid = node_guid
        self.item_guid = item_guid


class SceneStateError(ValueError):
    """Raised when declared durable scene state is invalid."""
