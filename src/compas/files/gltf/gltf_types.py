"""Shared types for glTF I/O."""

from typing import Any
from typing import Literal

GLTFFormat = Literal["gltf", "glb"]
GLTFJson = dict[str, Any]
AccessorData = Any


class GLTFConversionWarning(UserWarning):
    """Warning emitted when scene content cannot be represented in glTF."""
