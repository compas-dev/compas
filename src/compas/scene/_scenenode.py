from uuid import UUID

from compas.datastructures import TreeNode


class SceneNode(TreeNode["SceneNode"]):
    """Private hierarchy node referencing a scene object by GUID."""

    def __init__(self, object_guid: UUID) -> None:
        super().__init__()
        self.object_guid = object_guid
