"""Encoded glTF output independent of target I/O."""

from dataclasses import dataclass
from dataclasses import field

from .gltf_types import GLTFFormat
from .gltf_types import GLTFJson


@dataclass
class GLTFPayload:
    """Serializable primary glTF data and adjacent resources."""

    format: GLTFFormat
    json: GLTFJson
    binary: bytes = b""
    resources: dict[str, bytes] = field(default_factory=dict)
